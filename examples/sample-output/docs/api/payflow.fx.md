<!-- docweave:begin module -->
# `payflow.fx`

Currency conversion.

Source: [`payflow/fx.py`](../../payflow/fx.py) · 18 lines · main authors: Lena Fischer (55%), Marco Rossi (45%)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`RATES`](#rates) | constant | Static rates against USD; replaced nightly by the treasury export. |
| [`convert`](#convert) | function | Convert a Decimal amount between currencies using the static rate table. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:RATES -->
<a id="rates"></a>
### `RATES` <sup>constant</sup>

```python
RATES = {'USD': Decimal('1'), 'EUR': Decimal('0.92'), 'GBP': Decimal('0.79')}
```

Static rates against USD; replaced nightly by the treasury export.

<details><summary>History and rationale (1)</summary>

- 2026-02-02 · **refactor** · Rename convert_currency to convert and switch to Decimal ([`e26ca74`](https://github.com/example/payflow/commit/e26ca745224008cf598a84ffa367fd8c8995181e), Lena Fischer)<br>*Why:* We decided to use Decimal instead of float because float rounding lost cents on large invoices.

</details>

<sub>[`payflow/fx.py:6`](../../payflow/fx.py#L6) · written by Lena Fischer (100%)</sub>
<!-- docweave:end sym:RATES -->

<!-- docweave:begin sym:convert -->
<a id="convert"></a>
### `convert` <sup>function</sup>

```python
def convert(amount, source, target)
```

Convert a Decimal amount between currencies using the static rate table.

| Parameter | Description |
| --- | --- |
| `amount` | Amount as a Decimal. |
| `source` | Currency code to convert from. |
| `target` | Currency code to convert to. |

<details><summary>History and rationale (3)</summary>

- 2026-02-02 · **refactor** · Rename convert_currency to convert and switch to Decimal ([`e26ca74`](https://github.com/example/payflow/commit/e26ca745224008cf598a84ffa367fd8c8995181e), Lena Fischer)<br>*Why:* We decided to use Decimal instead of float because float rounding lost cents on large invoices.
- 2026-02-01 · **chat** · Heads up: `convert_currency` is going away. We decided to move money maths to Decimal because float rounding lost cents… (`#slack-payments`, lena)<br>*Why:* We decided to move money maths to Decimal because float rounding lost cents on large invoices.
- 2026-01-12 · **feature** · Add convert_currency with a static rate table ([`11f8f01`](https://github.com/example/payflow/commit/11f8f013cdce9502794e097e10f16512216a63db), Marco Rossi)

</details>

<sub>[`payflow/fx.py:9`](../../payflow/fx.py#L9) · complexity 1 · written by Marco Rossi (56%), Lena Fischer (44%)</sub>
<!-- docweave:end sym:convert -->
