<!-- docweave:begin module -->
# `payflow.ledger`

An append-only ledger of money movements.

Source: [`payflow/ledger.py`](../../payflow/ledger.py) · 34 lines · main authors: Priya Nair (63%), Lena Fischer (23%), Marco Rossi (13%)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`Ledger`](#ledger) | class | Records charges and refunds and reports the running balance. |
| [`Ledger.record`](#ledger-record) | method | Append an entry. |
| [`Ledger.balance`](#ledger-balance) | method | Return the current balance. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:Ledger -->
<a id="ledger"></a>
### `Ledger` <sup>class</sup>

```python
class Ledger
```

Records charges and refunds and reports the running balance.

<details><summary>History and rationale (1)</summary>

- 2026-01-05 · **feature** · Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair)

</details>

<sub>[`payflow/ledger.py:4`](../../payflow/ledger.py#L4) · written by Priya Nair (100%)</sub>
<!-- docweave:end sym:Ledger -->

<!-- docweave:begin sym:Ledger.record -->
<a id="ledger-record"></a>
#### `Ledger.record` <sup>method</sup>

```python
def record(self, kind, amount)
```

Append an entry.

| Parameter | Description |
| --- | --- |
| `kind` | Either charge or refund. |
| `amount` | Amount in minor units. |

**Raises:** `ValueError`

<details><summary>History and rationale (2)</summary>

- 2026-02-18 · **fix** · Stop recomputing the balance on every call ([`b918916`](https://github.com/example/payflow/commit/b91891625222546838299975c9debd9f8570554c), Lena Fischer)<br>*Why:* Large merchant accounts timed out because balance() rescanned every entry.
- 2026-01-05 · **feature** · Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair)

</details>

<sub>[`payflow/ledger.py:12`](../../payflow/ledger.py#L12) · complexity 3 · written by Priya Nair (58%), Marco Rossi (33%), Lena Fischer (8%)</sub>
<!-- docweave:end sym:Ledger.record -->

<!-- docweave:begin sym:Ledger.balance -->
<a id="ledger-balance"></a>
#### `Ledger.balance` <sup>method</sup>

```python
def balance(self)
```

> ⚠️ **Docs may be out of date** (medium): `Ledger.balance`: 80% of its code changed after the docstring was last edited
> - 2026-02-18 b918916 (fix, Lena Fischer): fix(ledger): stop recomputing the balance on every call

Return the current balance.

Recomputed from every entry on each call, so it is always consistent.

<details><summary>History and rationale (3)</summary>

- 2026-02-18 · **fix** · Stop recomputing the balance on every call ([`b918916`](https://github.com/example/payflow/commit/b91891625222546838299975c9debd9f8570554c), Lena Fischer)<br>*Why:* Large merchant accounts timed out because balance() rescanned every entry.
- 2026-02-18 · **chat** · Ledger.balance was rescanning every entry, which timed out for the big merchant accounts, so it is cached now instead o… (`#slack-payments`, priya)<br>*Why:* Ledger.balance was rescanning every entry, which timed out for the big merchant accounts, so it is cached now instead of recomputed.
- 2026-01-05 · **feature** · Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair)

</details>

<sub>[`payflow/ledger.py:25`](../../payflow/ledger.py#L25) · complexity 3 · written by Priya Nair (56%), Lena Fischer (44%)</sub>
<!-- docweave:end sym:Ledger.balance -->
