<!-- docweave:begin module -->
# `web.cart`

Cart maths shared by the checkout page.

Source: [`web/cart.js`](../../web/cart.js) · 24 lines · main authors: Priya Nair (81%), Marco Rossi (19%)

**Imports:** [`web.money`](web.money.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`total`](#total) | function | Sum the line items of a cart. |
| [`renderTotal`](#rendertotal) | function | Render the cart total for display. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:total -->
<a id="total"></a>
### `total` <sup>function</sup>

```ts
export function total(items, taxRate = 0)
```

> ⚠️ **Docs may be out of date** (high): `total`: its signature and 75% of its code changed after the docstring was last edited
> - 2026-03-03 4b6f7d3 (fix, Marco Rossi): fix(web): include tax when computing cart totals (#7)

> ⚠️ **Docs may be out of date** (medium): `total` does not document parameter(s) `taxRate`

Sum the line items of a cart.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `items` | `Array<{price: number, qty: number}>` |  | Line items. |
| `taxRate` |  | `0` |  |

**Returns:** Total in minor units.

<details><summary>History and rationale (3)</summary>

- 2026-03-03 · **pr** · Include tax in cart totals ([`pr:7`](https://github.com/example/payflow/pull/7), marco)<br>*Why:* The cart showed net prices while the provider charged gross, which caused support tickets about being overcharged. `total` now takes a tax rate so that the cart and the charge agree.
- 2026-03-03 · **fix** · Include tax when computing cart totals ([`4b6f7d3`](https://github.com/example/payflow/commit/4b6f7d3140256995f94a6ea17f30b6e0617aca4e), Marco Rossi)<br>*Why:* The cart showed net prices while the provider charged gross, which caused support tickets.
- 2026-02-25 · **feature** · Add cart totals for the checkout page ([`a638ecc`](https://github.com/example/payflow/commit/a638eccd52b0680dd3d52f13cd0a225f40fff116), Priya Nair)

</details>

<sub>[`web/cart.js:12`](../../web/cart.js#L12) · complexity 1 · written by Priya Nair (67%), Marco Rossi (33%)</sub>
<!-- docweave:end sym:total -->

<!-- docweave:begin sym:renderTotal -->
<a id="rendertotal"></a>
### `renderTotal` <sup>function</sup>

```ts
export const renderTotal = (items, currency) =>
```

Render the cart total for display.

| Parameter | Type | Description |
| --- | --- | --- |
| `items` | `Array` | Line items. |
| `currency` | `string` | ISO currency code. |

**Returns:** Formatted total.

<details><summary>History and rationale (2)</summary>

- 2026-03-03 · **pr** · Include tax in cart totals ([`pr:7`](https://github.com/example/payflow/pull/7), marco)<br>*Why:* The cart showed net prices while the provider charged gross, which caused support tickets about being overcharged. `total` now takes a tax rate so that the cart and the charge agree.
- 2026-02-25 · **feature** · Add cart totals for the checkout page ([`a638ecc`](https://github.com/example/payflow/commit/a638eccd52b0680dd3d52f13cd0a225f40fff116), Priya Nair)

</details>

<sub>[`web/cart.js:23`](../../web/cart.js#L23) · complexity 1 · written by Priya Nair (100%)</sub>
<!-- docweave:end sym:renderTotal -->
