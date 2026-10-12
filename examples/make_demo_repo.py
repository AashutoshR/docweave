"""Build a small git repository with a realistic history, for trying DocWeave out.

    python examples/make_demo_repo.py path/to/new/folder
    docweave generate --root path/to/new/folder

The fictional "payflow" project is written by three people over three months. Its history plants
exactly the situations DocWeave exists to catch: a signature that changed without its docstring,
a function renamed while the README still uses the old name, a behaviour change that left a
docstring describing the old implementation, a reformat that must *not* be flagged, and so on.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PRIYA, MARCO, LENA = "Priya Nair", "Marco Rossi", "Lena Fischer"

GATEWAY = '''"""Talk to the card provider."""

import time

PROVIDER_URL = "https://api.cardprovider.example/v2"


class ProviderError(Exception):
    """The card provider rejected or failed a request."""


def send(payload):
    """Send one request to the provider and return its JSON reply."""
    return {"status": 200, "id": "ch_" + str(payload["amount"])}


def charge(amount, currency):
    """Charge a card.

    Args:
        amount: Amount in minor units (cents).
        currency: ISO 4217 currency code.

    Returns:
        The provider's charge id.
    """
    reply = send({"amount": amount, "currency": currency})
    if reply["status"] != 200:
        raise ProviderError(reply["status"])
    return reply["id"]


def legacy_charge(card_number, amount):
    """Charge using the v1 API. Kept for the old checkout page."""
    return charge(amount, "USD")


def refund(charge_id, reason):
    """Refund a charge.

    Args:
        charge_id: Id returned by ``charge``.
        reason: Free-text reason shown to the customer.
    """
    send({"refund": charge_id, "reason": reason, "amount": 0})
'''

LEDGER = '''"""An append-only ledger of money movements."""


class Ledger:
    """Records charges and refunds and reports the running balance."""

    def __init__(self):
        self.entries = []

    def record(self, kind, amount):
        """Append an entry.

        Args:
            kind: Either charge or refund.
            amount: Amount in minor units.
        """
        if kind not in ('charge', 'refund'):
            raise ValueError('unknown kind: ' + kind)
        sign = 1 if kind == 'charge' else -1
        self.entries.append({'kind': kind, 'amount': sign * amount})

    def balance(self):
        """Return the current balance.

        Recomputed from every entry on each call, so it is always consistent.
        """
        total = 0
        for entry in self.entries:
            total += entry['amount']
        return total
'''

FX = '''"""Currency conversion."""

RATES = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79}


def convert_currency(amount, source, target):
    """Convert an amount between currencies using the static rate table.

    Args:
        amount: Amount as a float.
        source: Currency code to convert from.
        target: Currency code to convert to.
    """
    return amount / RATES[source] * RATES[target]
'''

FX_DECIMAL = '''"""Currency conversion."""

from decimal import Decimal

# Static rates against USD; replaced nightly by the treasury export.
RATES = {"USD": Decimal("1"), "EUR": Decimal("0.92"), "GBP": Decimal("0.79")}


def convert(amount, source, target):
    """Convert a Decimal amount between currencies using the static rate table.

    Args:
        amount: Amount as a Decimal.
        source: Currency code to convert from.
        target: Currency code to convert to.
    """
    return (amount / RATES[source] * RATES[target]).quantize(Decimal("0.01"))
'''

README = '''# payflow

Small payments service used by the checkout.

## Usage

Call `charge` with an amount in cents and a currency code; it returns the provider's charge id.
Older integrations can still use `legacy_charge()`.

Background on the ledger design is in `notes/ledger.md`.

## API at a glance

<!-- docweave:begin modules -->
<!-- docweave:end modules -->
'''

CART = '''/**
 * Cart maths shared by the checkout page.
 */

import { formatMoney } from './money';

/**
 * Sum the line items of a cart.
 * @param {Array<{price: number, qty: number}>} items - Line items.
 * @returns {number} Total in minor units.
 */
export function total(items) {
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}

/**
 * Render the cart total for display.
 * @param {Array} items - Line items.
 * @param {string} currency - ISO currency code.
 * @returns {string} Formatted total.
 */
export const renderTotal = (items, currency) => formatMoney(total(items), currency);
'''

MONEY = '''export function formatMoney(amount, currency) {
  return new Intl.NumberFormat('en', { style: 'currency', currency }).format(amount / 100);
}
'''

PULL_REQUESTS = [
    {
        "number": 4, "title": "Retry charges on 429", "author": {"login": "priya"},
        "mergedAt": "2026-01-20T10:30:00Z", "url": "https://github.com/example/payflow/pull/4",
        "body": "Checkout failed outright whenever the provider answered 429.\n\n"
                "The provider rate limits bursts, not sustained load, so a short wait almost always succeeds. "
                "We chose exponential backoff rather than a fixed delay because a fixed delay re-synchronises "
                "all the retrying checkouts into another burst.",
    },
    {
        "number": 7, "title": "Include tax in cart totals", "author": {"login": "marco"},
        "mergedAt": "2026-03-03T15:00:00Z", "url": "https://github.com/example/payflow/pull/7",
        "body": "The cart showed net prices while the provider charged gross, which caused support tickets "
                "about being overcharged. `total` now takes a tax rate so that the cart and the charge agree.",
    },
]

CHAT = [
    {"user_name": "lena", "ts": "1769940000.000100",
     "text": "Heads up: `convert_currency` is going away. We decided to move money maths to Decimal because "
             "float rounding lost cents on large invoices. The new name is `convert`."},
    {"user_name": "marco", "ts": "1769943600.000200",
     "text": "Makes sense. Lunch at 12:30?"},
    {"user_name": "priya", "ts": "1771400000.000300",
     "text": "Ledger.balance was rescanning every entry, which timed out for the big merchant accounts, "
             "so it is cached now instead of recomputed."},
]


def _git(repo: Path, *args: str, env: dict | None = None) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env={**os.environ, **(env or {})})


class Story:
    """Applies a sequence of file edits, committing each as a different author on a given date."""

    def __init__(self, repo: Path) -> None:
        self.repo = repo
        self.files: dict[str, str] = {}

    def write(self, path: str, text: str) -> None:
        self.files[path] = text
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")

    def edit(self, path: str, old: str, new: str) -> None:
        assert old in self.files[path], f"{old!r} not found in {path}"
        self.write(path, self.files[path].replace(old, new))

    def delete(self, path: str) -> None:
        del self.files[path]
        (self.repo / path).unlink()

    def commit(self, author: str, date: str, message: str, tag: str | None = None) -> None:
        stamp = f"{date}T10:00:00+00:00"
        email = author.split()[0].lower() + "@example.com"
        env = {
            "GIT_AUTHOR_NAME": author, "GIT_AUTHOR_EMAIL": email, "GIT_AUTHOR_DATE": stamp,
            "GIT_COMMITTER_NAME": author, "GIT_COMMITTER_EMAIL": email, "GIT_COMMITTER_DATE": stamp,
        }
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-q", "-m", message, env=env)
        if tag:
            _git(self.repo, "tag", tag)


def build(repo: Path) -> Path:
    """Create the demo repository at ``repo`` (which must not exist or be empty)."""
    repo = Path(repo)
    repo.mkdir(parents=True, exist_ok=True)
    if any(repo.iterdir()):
        raise SystemExit(f"{repo} is not empty")
    _git(repo, "init", "-q", "-b", "main")
    for key, value in (("core.autocrlf", "false"), ("commit.gpgsign", "false"), ("user.name", "demo"), ("user.email", "demo@example.com")):
        _git(repo, "config", key, value)
    _git(repo, "remote", "add", "origin", "https://github.com/example/payflow.git")
    s = Story(repo)

    s.write("payflow/__init__.py", '"""payflow: charge cards, convert currencies and keep a ledger."""\n')
    s.write("payflow/gateway.py", GATEWAY)
    s.write("payflow/ledger.py", LEDGER)
    s.write("README.md", README)
    s.write("notes/ledger.md", "# Ledger design\n\nEntries are append-only so that audits can replay history.\n")
    s.commit(PRIYA, "2026-01-05", "feat: initial gateway and ledger")

    s.write("payflow/fx.py", FX)
    s.edit("README.md", "Background on", "To show prices in the shopper's currency use `convert_currency`.\n\nBackground on")
    s.commit(MARCO, "2026-01-12", "feat(fx): add convert_currency with a static rate table")

    # The signature and body change; the docstring is left behind.
    s.edit("payflow/gateway.py", "def charge(amount, currency):", "def charge(amount, currency, retries=3):")
    s.edit(
        "payflow/gateway.py",
        '''    reply = send({"amount": amount, "currency": currency})
    if reply["status"] != 200:
        raise ProviderError(reply["status"])
    return reply["id"]
''',
        '''    for attempt in range(retries + 1):
        reply = send({"amount": amount, "currency": currency})
        if reply["status"] == 429 and attempt < retries:
            time.sleep(2 ** attempt)
            continue
        if reply["status"] != 200:
            raise ProviderError(reply["status"])
        return reply["id"]
''',
    )
    s.commit(PRIYA, "2026-01-20", "fix(gateway): retry charges on 429 (#4)\n\n"
             "Checkout failed outright on a 429. The provider rate limits bursts, so we now back off\n"
             "exponentially instead of failing the whole checkout.")

    # A rename, described in plain English rather than with a conventional prefix.
    s.write("payflow/fx.py", FX_DECIMAL)
    s.commit(LENA, "2026-02-02", "Rename convert_currency to convert and switch to Decimal\n\n"
             "We decided to use Decimal instead of float because float rounding lost cents on\n"
             "large invoices.")

    # Pure formatting: touches most of record() but must not make its docstring look stale.
    s.edit("payflow/ledger.py", "('charge', 'refund')", '("charge", "refund")')
    s.edit("payflow/ledger.py", "raise ValueError('unknown kind: ' + kind)", 'raise ValueError("unknown kind: " + kind)')
    s.edit("payflow/ledger.py", "sign = 1 if kind == 'charge' else -1", 'sign = 1 if kind == "charge" else -1')
    s.edit("payflow/ledger.py", "{'kind': kind, 'amount': sign * amount}", '{"kind": kind, "amount": sign * amount}')
    s.edit("payflow/ledger.py", "entry['amount']", 'entry["amount"]')
    s.commit(MARCO, "2026-02-10", "style: reformat ledger with black")

    # Behaviour changes underneath a docstring that still describes the old implementation.
    s.edit("payflow/ledger.py", "        self.entries = []\n", "        self.entries = []\n        self._balance = 0\n        self._dirty = False\n")
    s.edit("payflow/ledger.py", '"amount": sign * amount})\n', '"amount": sign * amount})\n        self._dirty = True\n')
    s.edit(
        "payflow/ledger.py",
        '''        total = 0
        for entry in self.entries:
            total += entry["amount"]
        return total
''',
        '''        if self._dirty:
            self._balance = sum(entry["amount"] for entry in self.entries)
            self._dirty = False
        return self._balance
''',
    )
    s.commit(LENA, "2026-02-18", "fix(ledger): stop recomputing the balance on every call\n\n"
             "Large merchant accounts timed out because balance() rescanned every entry. The total is\n"
             "now cached and only rebuilt after a write.", tag="v0.1.0")

    s.write("web/cart.js", CART)
    s.write("web/money.js", MONEY)
    s.commit(PRIYA, "2026-02-25", "feat(web): add cart totals for the checkout page")

    s.edit("web/cart.js", "export function total(items) {\n  return items.reduce((sum, item) => sum + item.price * item.qty, 0);\n",
           "export function total(items, taxRate = 0) {\n  const net = items.reduce((sum, item) => sum + item.price * item.qty, 0);\n  return Math.round(net * (1 + taxRate));\n")
    s.commit(MARCO, "2026-03-03", "fix(web): include tax when computing cart totals (#7)\n\n"
             "The cart showed net prices while the provider charged gross, which caused support tickets.")

    s.edit("payflow/gateway.py", "    for attempt in range(retries + 1):", '    if amount <= 0:\n        raise ValueError("amount must be positive")\n    for attempt in range(retries + 1):')
    s.commit(PRIYA, "2026-03-10", "Harden charge against negative amounts\n\n"
             "The provider treats a negative amount as a credit, so a crafted request could issue itself\n"
             "a refund. Validate before sending to prevent that.")

    s.edit("payflow/gateway.py", "def refund(charge_id, reason):", "def refund(charge_id):")
    s.edit("payflow/gateway.py", '"reason": reason, ', "")
    s.commit(LENA, "2026-03-14", "refactor(gateway): drop the refund reason, the provider ignores it")

    s.edit("payflow/gateway.py", '''def legacy_charge(card_number, amount):
    """Charge using the v1 API. Kept for the old checkout page."""
    return charge(amount, "USD")


''', "")
    s.commit(MARCO, "2026-03-20", "refactor!: remove legacy_charge\n\n"
             "BREAKING CHANGE: the provider switched off the v1 endpoint; use charge instead.")

    s.delete("notes/ledger.md")
    s.commit(PRIYA, "2026-03-22", "docs: drop outdated ledger notes")

    s.write("comms/github-prs.json", json.dumps(PULL_REQUESTS, indent=2) + "\n")
    s.write("comms/slack-payments.json", json.dumps(CHAT, indent=2) + "\n")
    s.commit(LENA, "2026-03-25", "chore: export PR and chat history")
    return repo


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(f"demo repository created at {build(Path(sys.argv[1]))}")
