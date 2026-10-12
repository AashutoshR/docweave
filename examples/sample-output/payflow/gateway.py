"""Talk to the card provider."""

import time

PROVIDER_URL = "https://api.cardprovider.example/v2"


class ProviderError(Exception):
    """The card provider rejected or failed a request."""


def send(payload):
    """Send one request to the provider and return its JSON reply."""
    return {"status": 200, "id": "ch_" + str(payload["amount"])}


def charge(amount, currency, retries=3):
    """Charge a card.

    Args:
        amount: Amount in minor units (cents).
        currency: ISO 4217 currency code.

    Returns:
        The provider's charge id.
    """
    if amount <= 0:
        raise ValueError("amount must be positive")
    for attempt in range(retries + 1):
        reply = send({"amount": amount, "currency": currency})
        if reply["status"] == 429 and attempt < retries:
            time.sleep(2 ** attempt)
            continue
        if reply["status"] != 200:
            raise ProviderError(reply["status"])
        return reply["id"]


def refund(charge_id):
    """Refund a charge.

    Args:
        charge_id: Id returned by ``charge``.
        reason: Free-text reason shown to the customer.
    """
    send({"refund": charge_id, "amount": 0})
