---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

コードレビューで「このファイルのコメントは整理したほうがいい」と言われました。コメントを見直して、整理後のコードと、各コメントをどう扱ったか（消した・移した・残した）を教えてください。

```rust
pub fn merge_orders(mut orders: Vec<Order>, refunds: &[Refund]) -> Vec<Order> {
    // orders と refunds をループする
    for order in &mut orders {
        // #128 の修正 (2024-03): 返金が無いのに内側のループを回していたのでガードを追加
        if refunds.is_empty() {
            continue;
        }
        for refund in refunds {
            // refund の id が一致したら金額を引く
            if refund.order_id == order.id {
                order.amount -= refund.amount;
            }
        }
    }
    // let old: i64 = orders.iter().map(|o| o.amount).sum();
    orders
}
```
