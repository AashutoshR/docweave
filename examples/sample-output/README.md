# payflow

Small payments service used by the checkout.

## Usage

Call `charge` with an amount in cents and a currency code; it returns the provider's charge id.
Older integrations can still use `legacy_charge()`.

To show prices in the shopper's currency use `convert_currency`.

Background on the ledger design is in `notes/ledger.md`.

## API at a glance

<!-- docweave:begin modules -->
| Module | What it does | Public API | Documented | Main authors |
| --- | --- | ---: | ---: | --- |
| [`payflow`](docs/api/payflow.md) | payflow: charge cards, convert currencies and keep a ledger. | 0 | - | - |
| [`payflow.fx`](docs/api/payflow.fx.md) | Currency conversion. | 1 | 100% | Lena Fischer (55%), Marco Rossi (45%) |
| [`payflow.gateway`](docs/api/payflow.gateway.md) | Talk to the card provider. | 4 | 100% | Priya Nair (94%), Lena Fischer (6%) |
| [`payflow.ledger`](docs/api/payflow.ledger.md) | An append-only ledger of money movements. | 3 | 100% | Priya Nair (63%), Lena Fischer (23%), Marco Rossi (13%) |
| [`web.cart`](docs/api/web.cart.md) | Cart maths shared by the checkout page. | 2 | 100% | Priya Nair (81%), Marco Rossi (19%) |
| [`web.money`](docs/api/web.money.md) | Defines `formatMoney`. | 1 | 0% | Priya Nair (100%) |
<!-- docweave:end modules -->
