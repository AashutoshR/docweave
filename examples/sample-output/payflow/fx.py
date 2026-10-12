"""Currency conversion."""

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
