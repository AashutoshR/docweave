<!-- docweave:begin title -->
# Changelog

Generated from commit history. Changes are grouped by what each commit *does*, classified from its message, and annotated with the public API it touches.
<!-- docweave:end title -->

<!-- docweave:begin release:Unreleased -->
## Unreleased

### ⚠️ Breaking changes

- Remove legacy_charge ([`0916746`](https://github.com/example/payflow/commit/091674695628a07fc80fd4264353e32b2ddec7d4), Marco Rossi) - [`charge`](api/payflow.gateway.md#charge)

### Features

- **web:** Add cart totals for the checkout page ([`a638ecc`](https://github.com/example/payflow/commit/a638eccd52b0680dd3d52f13cd0a225f40fff116), Priya Nair) - [`renderTotal`](api/web.cart.md#rendertotal), [`formatMoney`](api/web.money.md#formatmoney), [`total`](api/web.cart.md#total)

### Fixes

- **web:** Include tax when computing cart totals ([`4b6f7d3`](https://github.com/example/payflow/commit/4b6f7d3140256995f94a6ea17f30b6e0617aca4e), Marco Rossi) - [`total`](api/web.cart.md#total)

### Security

- Harden charge against negative amounts ([`3038806`](https://github.com/example/payflow/commit/3038806f85fcbe38126b21feadfcc3bf9ad3bae7), Priya Nair) - [`charge`](api/payflow.gateway.md#charge)

### Refactoring

- **gateway:** Drop the refund reason, the provider ignores it ([`5748d1e`](https://github.com/example/payflow/commit/5748d1e7fd09f2aac26a3b67d1df24d99369baa4), Lena Fischer) - [`refund`](api/payflow.gateway.md#refund)
<!-- docweave:end release:Unreleased -->

<!-- docweave:begin release:v0.1.0 -->
## v0.1.0 - 2026-02-18

### Features

- **fx:** Add convert_currency with a static rate table ([`11f8f01`](https://github.com/example/payflow/commit/11f8f013cdce9502794e097e10f16512216a63db), Marco Rossi) - [`convert`](api/payflow.fx.md#convert)
- Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair) - [`Ledger`](api/payflow.ledger.md#ledger), [`PROVIDER_URL`](api/payflow.gateway.md#provider-url), [`ProviderError`](api/payflow.gateway.md#providererror)

### Fixes

- **ledger:** Stop recomputing the balance on every call ([`b918916`](https://github.com/example/payflow/commit/b91891625222546838299975c9debd9f8570554c), Lena Fischer) - [`Ledger.balance`](api/payflow.ledger.md#ledger-balance)
- **gateway:** Retry charges on 429 ([`c8bf421`](https://github.com/example/payflow/commit/c8bf42139008cd5dcf0da94eb16f25ba814709d4), Priya Nair) - [`charge`](api/payflow.gateway.md#charge)

### Refactoring

- Rename convert_currency to convert and switch to Decimal ([`e26ca74`](https://github.com/example/payflow/commit/e26ca745224008cf598a84ffa367fd8c8995181e), Lena Fischer) - [`RATES`](api/payflow.fx.md#rates), [`convert`](api/payflow.fx.md#convert)
<!-- docweave:end release:v0.1.0 -->
