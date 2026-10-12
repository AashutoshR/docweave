<!-- docweave:begin title -->
# Decision log

Design decisions and their reasoning, mined from commit messages, pull requests, chat and notes. Each entry links the code it shaped.
<!-- docweave:end title -->

<!-- docweave:begin decision:pr_7 -->
### Include tax in cart totals

2026-03-03 · pr [`pr:7`](https://github.com/example/payflow/pull/7) · marco

> The cart showed net prices while the provider charged gross, which caused support tickets about being overcharged.
> `total` now takes a tax rate so that the cart and the charge agree.

Shaped: [`total`](api/web.cart.md#total), [`renderTotal`](api/web.cart.md#rendertotal)
<!-- docweave:end decision:pr_7 -->

<!-- docweave:begin decision:chat_slack-payments_1771400000.000300 -->
### Ledger.balance was rescanning every entry, which timed out for the big merchant accounts,…

2026-02-18 · chat `#slack-payments` · priya

> Ledger.balance was rescanning every entry, which timed out for the big merchant accounts, so it is cached now instead of recomputed.

Shaped: [`Ledger.balance`](api/payflow.ledger.md#ledger-balance)
<!-- docweave:end decision:chat_slack-payments_1771400000.000300 -->

<!-- docweave:begin decision:commit_e26ca745224008cf598a84ffa367fd8c8995181e -->
### Rename convert_currency to convert and switch to Decimal

2026-02-02 · commit [`e26ca74`](https://github.com/example/payflow/commit/e26ca745224008cf598a84ffa367fd8c8995181e) · Lena Fischer

> We decided to use Decimal instead of float because float rounding lost cents on large invoices.

Shaped: [`RATES`](api/payflow.fx.md#rates), [`convert`](api/payflow.fx.md#convert)
<!-- docweave:end decision:commit_e26ca745224008cf598a84ffa367fd8c8995181e -->

<!-- docweave:begin decision:chat_slack-payments_1769940000.000100 -->
### Heads up: `convert_currency` is going away.

2026-02-01 · chat `#slack-payments` · lena

> We decided to move money maths to Decimal because float rounding lost cents on large invoices.

Shaped: [`convert`](api/payflow.fx.md#convert)
<!-- docweave:end decision:chat_slack-payments_1769940000.000100 -->

<!-- docweave:begin decision:pr_4 -->
### Retry charges on 429

2026-01-20 · pr [`pr:4`](https://github.com/example/payflow/pull/4) · priya

> The provider rate limits bursts, not sustained load, so a short wait almost always succeeds.
> We chose exponential backoff rather than a fixed delay because a fixed delay re-synchronises all the retrying checkouts into another burst.

Shaped: [`charge`](api/payflow.gateway.md#charge)
<!-- docweave:end decision:pr_4 -->

<!-- docweave:begin decision:commit_c8bf42139008cd5dcf0da94eb16f25ba814709d4 -->
### Retry charges on 429

2026-01-20 · commit [`c8bf421`](https://github.com/example/payflow/commit/c8bf42139008cd5dcf0da94eb16f25ba814709d4) · Priya Nair

> The provider rate limits bursts, so we now back off exponentially instead of failing the whole checkout.

Shaped: [`charge`](api/payflow.gateway.md#charge)
<!-- docweave:end decision:commit_c8bf42139008cd5dcf0da94eb16f25ba814709d4 -->
