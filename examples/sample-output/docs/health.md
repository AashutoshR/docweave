<!-- docweave:begin title -->
# Documentation health
<!-- docweave:end title -->

<!-- docweave:begin score -->
**Documentation health: 36/100** · 91% of 11 public symbols documented · 11 drift issues

The score is 40% coverage (public symbols with documentation) and 60% freshness (drift issues, weighted by severity).
<!-- docweave:end score -->

<!-- docweave:begin issues:high -->
## 🔴 High (6)

- [`README.md:8`](../README.md#L8) **dangling-reference** - `legacy_charge` is mentioned here but no longer exists in the code
  - removed in 0916746 on 2026-03-20 by Marco Rossi: "refactor!: remove legacy_charge"
  - did you mean `charge`?
- [`README.md:10`](../README.md#L10) **dangling-reference** - `convert_currency` is mentioned here but no longer exists in the code
  - removed in e26ca74 on 2026-02-02 by Lena Fischer: "Rename convert_currency to convert and switch to Decimal"
  - did you mean `convert`?
- [`payflow/gateway.py:18`](../payflow/gateway.py#L18) **stale-docstring** - `charge`: its signature and 64% of its code changed after the docstring was last edited
  - 2026-03-10 3038806 (security, Priya Nair): Harden charge against negative amounts
  - 2026-01-20 c8bf421 (fix, Priya Nair): fix(gateway): retry charges on 429 (#4)
- [`payflow/gateway.py:40`](../payflow/gateway.py#L40) **param-not-in-signature** - `refund` documents `reason`, which is not in its signature
- [`payflow/gateway.py:40`](../payflow/gateway.py#L40) **stale-docstring** - `refund`: its signature and 50% of its code changed after the docstring was last edited
  - 2026-03-14 5748d1e (refactor, Lena Fischer): refactor(gateway): drop the refund reason, the provider ignores it
- [`web/cart.js:7`](../web/cart.js#L7) **stale-docstring** - `total`: its signature and 75% of its code changed after the docstring was last edited
  - 2026-03-03 4b6f7d3 (fix, Marco Rossi): fix(web): include tax when computing cart totals (#7)
<!-- docweave:end issues:high -->

<!-- docweave:begin issues:medium -->
## 🟠 Medium (5)

- [`README.md:7`](../README.md#L7) **stale-prose** - this text mentions `charge`, but its signature changed since the line was written (2026-01-05)
  - 2026-03-10 3038806 (security, Priya Nair): Harden charge against negative amounts
  - 2026-01-20 c8bf421 (fix, Priya Nair): fix(gateway): retry charges on 429 (#4)
- [`README.md:12`](../README.md#L12) **missing-path** - `notes/ledger.md` is referenced here but was deleted
  - deleted in 2bea542 on 2026-03-22 by Priya Nair: "docs: drop outdated ledger notes"
- [`payflow/gateway.py:18`](../payflow/gateway.py#L18) **param-undocumented** - `charge` does not document parameter(s) `retries`
- [`payflow/ledger.py:26`](../payflow/ledger.py#L26) **stale-docstring** - `Ledger.balance`: 80% of its code changed after the docstring was last edited
  - 2026-02-18 b918916 (fix, Lena Fischer): fix(ledger): stop recomputing the balance on every call
- [`web/cart.js:7`](../web/cart.js#L7) **param-undocumented** - `total` does not document parameter(s) `taxRate`
<!-- docweave:end issues:medium -->

<!-- docweave:begin legend -->
## What the checks mean

- **dangling-reference** - Hand-written docs mention code that no longer exists.
- **missing-path** - Hand-written docs point at a file that is not there.
- **param-not-in-signature** - The docstring documents a parameter the function no longer accepts.
- **param-undocumented** - The docstring lists parameters but leaves some out.
- **stale-docstring** - The code changed in later commits but its docstring did not.
- **stale-prose** - Hand-written docs describe code that has substantially changed since they were written.
<!-- docweave:end legend -->

<!-- docweave:begin coverage -->
## Coverage

| Module | Documented | Undocumented public symbols |
| --- | ---: | --- |
| `payflow.fx` | 1/1 |  |
| `payflow.gateway` | 4/4 |  |
| `payflow.ledger` | 3/3 |  |
| `web.cart` | 2/2 |  |
| `web.money` | 0/1 | `formatMoney` |
<!-- docweave:end coverage -->
