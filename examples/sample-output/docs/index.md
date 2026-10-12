<!-- docweave:begin title -->
# payflow3 documentation
<!-- docweave:end title -->

<!-- docweave:begin health -->
**Documentation health: 36/100** · 91% of 11 public symbols documented · 11 drift issues ([report](health.md))
<!-- docweave:end health -->

<!-- docweave:begin overview -->
6 modules · 14 symbols · 129 lines of javascript + python

[Architecture](architecture.md) · [Health report](health.md) · [Changelog](CHANGELOG.md) · [Decision log](decisions.md)
<!-- docweave:end overview -->

<!-- docweave:begin modules -->
## Modules

| Module | What it does | Public API | Documented | Main authors |
| --- | --- | ---: | ---: | --- |
| [`payflow`](api/payflow.md) | payflow: charge cards, convert currencies and keep a ledger. | 0 | - | - |
| [`payflow.fx`](api/payflow.fx.md) | Currency conversion. | 1 | 100% | Lena Fischer (55%), Marco Rossi (45%) |
| [`payflow.gateway`](api/payflow.gateway.md) | Talk to the card provider. | 4 | 100% | Priya Nair (94%), Lena Fischer (6%) |
| [`payflow.ledger`](api/payflow.ledger.md) | An append-only ledger of money movements. | 3 | 100% | Priya Nair (63%), Lena Fischer (23%), Marco Rossi (13%) |
| [`web.cart`](api/web.cart.md) | Cart maths shared by the checkout page. | 2 | 100% | Priya Nair (81%), Marco Rossi (19%) |
| [`web.money`](api/web.money.md) | Defines `formatMoney`. | 1 | 0% | Priya Nair (100%) |
<!-- docweave:end modules -->

<!-- docweave:begin recent -->
## Recent changes

- 2026-03-20 · **refactor** · Remove legacy_charge ([`0916746`](https://github.com/example/payflow/commit/091674695628a07fc80fd4264353e32b2ddec7d4), Marco Rossi) - touches [`charge`](api/payflow.gateway.md#charge)
- 2026-03-14 · **refactor** · Drop the refund reason, the provider ignores it ([`5748d1e`](https://github.com/example/payflow/commit/5748d1e7fd09f2aac26a3b67d1df24d99369baa4), Lena Fischer) - touches [`refund`](api/payflow.gateway.md#refund)
- 2026-03-10 · **security** · Harden charge against negative amounts ([`3038806`](https://github.com/example/payflow/commit/3038806f85fcbe38126b21feadfcc3bf9ad3bae7), Priya Nair) - touches [`charge`](api/payflow.gateway.md#charge)
- 2026-03-03 · **fix** · Include tax when computing cart totals ([`4b6f7d3`](https://github.com/example/payflow/commit/4b6f7d3140256995f94a6ea17f30b6e0617aca4e), Marco Rossi) - touches [`total`](api/web.cart.md#total)
- 2026-02-25 · **feature** · Add cart totals for the checkout page ([`a638ecc`](https://github.com/example/payflow/commit/a638eccd52b0680dd3d52f13cd0a225f40fff116), Priya Nair) - touches [`renderTotal`](api/web.cart.md#rendertotal), [`formatMoney`](api/web.money.md#formatmoney), [`total`](api/web.cart.md#total)
- 2026-02-18 · **fix** · Stop recomputing the balance on every call ([`b918916`](https://github.com/example/payflow/commit/b91891625222546838299975c9debd9f8570554c), Lena Fischer) - touches [`Ledger.balance`](api/payflow.ledger.md#ledger-balance)
- 2026-02-02 · **refactor** · Rename convert_currency to convert and switch to Decimal ([`e26ca74`](https://github.com/example/payflow/commit/e26ca745224008cf598a84ffa367fd8c8995181e), Lena Fischer) - touches [`RATES`](api/payflow.fx.md#rates), [`convert`](api/payflow.fx.md#convert)
- 2026-01-20 · **fix** · Retry charges on 429 ([`c8bf421`](https://github.com/example/payflow/commit/c8bf42139008cd5dcf0da94eb16f25ba814709d4), Priya Nair) - touches [`charge`](api/payflow.gateway.md#charge)
<!-- docweave:end recent -->
