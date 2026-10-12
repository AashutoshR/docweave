<!-- docweave:begin module -->
# `payflow.gateway`

Talk to the card provider.

Source: [`payflow/gateway.py`](../../payflow/gateway.py) · 47 lines · main authors: Priya Nair (94%), Lena Fischer (6%)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`PROVIDER_URL`](#provider-url) | constant | Provider url setting. |
| [`ProviderError`](#providererror) | class | The card provider rejected or failed a request. |
| [`send`](#send) | function | Send one request to the provider and return its JSON reply. |
| [`charge`](#charge) | function | Charge a card. |
| [`refund`](#refund) | function | Refund a charge. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:PROVIDER_URL -->
<a id="provider-url"></a>
### `PROVIDER_URL` <sup>constant</sup>

```python
PROVIDER_URL = 'https://api.cardprovider.example/v2'
```

Provider url setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-01-05 · **feature** · Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair)

</details>

<sub>[`payflow/gateway.py:5`](../../payflow/gateway.py#L5) · written by Priya Nair (100%)</sub>
<!-- docweave:end sym:PROVIDER_URL -->

<!-- docweave:begin sym:ProviderError -->
<a id="providererror"></a>
### `ProviderError` <sup>class</sup>

```python
class ProviderError(Exception)
```

The card provider rejected or failed a request.

<details><summary>History and rationale (1)</summary>

- 2026-01-05 · **feature** · Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair)

</details>

<sub>[`payflow/gateway.py:8`](../../payflow/gateway.py#L8) · written by Priya Nair (100%)</sub>
<!-- docweave:end sym:ProviderError -->

<!-- docweave:begin sym:send -->
<a id="send"></a>
### `send` <sup>function</sup>

```python
def send(payload)
```

Send one request to the provider and return its JSON reply.

| Parameter |
| --- |
| `payload` |

<details><summary>History and rationale (1)</summary>

- 2026-01-05 · **feature** · Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair)

</details>

<sub>[`payflow/gateway.py:12`](../../payflow/gateway.py#L12) · complexity 1 · written by Priya Nair (100%)</sub>
<!-- docweave:end sym:send -->

<!-- docweave:begin sym:charge -->
<a id="charge"></a>
### `charge` <sup>function</sup>

```python
def charge(amount, currency, retries=3)
```

> ⚠️ **Docs may be out of date** (high): `charge`: its signature and 64% of its code changed after the docstring was last edited
> - 2026-03-10 3038806 (security, Priya Nair): Harden charge against negative amounts
> - 2026-01-20 c8bf421 (fix, Priya Nair): fix(gateway): retry charges on 429 (#4)

> ⚠️ **Docs may be out of date** (medium): `charge` does not document parameter(s) `retries`

Charge a card.

| Parameter | Default | Description |
| --- | --- | --- |
| `amount` |  | Amount in minor units (cents). |
| `currency` |  | ISO 4217 currency code. |
| `retries` | `3` |  |

**Returns:** The provider's charge id.

**Raises:** `ProviderError`; `ValueError`

<details><summary>History and rationale (5)</summary>

- 2026-03-20 · **refactor** · Remove legacy_charge ([`0916746`](https://github.com/example/payflow/commit/091674695628a07fc80fd4264353e32b2ddec7d4), Marco Rossi)
- 2026-03-10 · **security** · Harden charge against negative amounts ([`3038806`](https://github.com/example/payflow/commit/3038806f85fcbe38126b21feadfcc3bf9ad3bae7), Priya Nair)<br>*Why:* The provider treats a negative amount as a credit, so a crafted request could issue itself a refund. Validate before sending to prevent that.
- 2026-01-20 · **pr** · Retry charges on 429 ([`pr:4`](https://github.com/example/payflow/pull/4), priya)<br>*Why:* The provider rate limits bursts, not sustained load, so a short wait almost always succeeds. We chose exponential backoff rather than a fixed delay because a fixed delay re-synchronises all the retrying checkouts into a…
- 2026-01-20 · **fix** · Retry charges on 429 ([`c8bf421`](https://github.com/example/payflow/commit/c8bf42139008cd5dcf0da94eb16f25ba814709d4), Priya Nair)<br>*Why:* The provider rate limits bursts, so we now back off exponentially instead of failing the whole checkout.
- 2026-01-05 · **feature** · Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair)

</details>

<sub>[`payflow/gateway.py:17`](../../payflow/gateway.py#L17) · complexity 6 · written by Priya Nair (100%)</sub>
<!-- docweave:end sym:charge -->

<!-- docweave:begin sym:refund -->
<a id="refund"></a>
### `refund` <sup>function</sup>

```python
def refund(charge_id)
```

> ⚠️ **Docs may be out of date** (high): `refund` documents `reason`, which is not in its signature

> ⚠️ **Docs may be out of date** (high): `refund`: its signature and 50% of its code changed after the docstring was last edited
> - 2026-03-14 5748d1e (refactor, Lena Fischer): refactor(gateway): drop the refund reason, the provider ignores it

Refund a charge.

| Parameter | Description |
| --- | --- |
| `charge_id` | Id returned by ``charge``. |

<details><summary>History and rationale (2)</summary>

- 2026-03-14 · **refactor** · Drop the refund reason, the provider ignores it ([`5748d1e`](https://github.com/example/payflow/commit/5748d1e7fd09f2aac26a3b67d1df24d99369baa4), Lena Fischer)
- 2026-01-05 · **feature** · Initial gateway and ledger ([`469585f`](https://github.com/example/payflow/commit/469585fe53bea53a0515e8f6b8e4339aaff6ecca), Priya Nair)

</details>

<sub>[`payflow/gateway.py:39`](../../payflow/gateway.py#L39) · complexity 1 · written by Priya Nair (75%), Lena Fischer (25%)</sub>
<!-- docweave:end sym:refund -->
