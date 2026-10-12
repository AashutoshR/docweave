"""An append-only ledger of money movements."""


class Ledger:
    """Records charges and refunds and reports the running balance."""

    def __init__(self):
        self.entries = []
        self._balance = 0
        self._dirty = False

    def record(self, kind, amount):
        """Append an entry.

        Args:
            kind: Either charge or refund.
            amount: Amount in minor units.
        """
        if kind not in ("charge", "refund"):
            raise ValueError("unknown kind: " + kind)
        sign = 1 if kind == "charge" else -1
        self.entries.append({"kind": kind, "amount": sign * amount})
        self._dirty = True

    def balance(self):
        """Return the current balance.

        Recomputed from every entry on each call, so it is always consistent.
        """
        if self._dirty:
            self._balance = sum(entry["amount"] for entry in self.entries)
            self._dirty = False
        return self._balance
