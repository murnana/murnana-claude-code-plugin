---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

コードレビューで「このファイルのコメントは整理したほうがいい」と言われました。コメントを見直して、整理後のコードと、各コメントをどう扱ったか（消した・移した・残した）を教えてください。

```cpp
void MergeOrders(std::vector<Order>& orders, const std::vector<Refund>& refunds) {
    // orders と refunds をループする
    for (auto& order : orders) {
        // #128 の修正 (2024-03): 返金が無いのに内側のループを回していたのでガードを追加
        if (refunds.empty()) {
            continue;
        }
        for (const auto& refund : refunds) {
            // refund の id が一致したら金額を引く
            if (refund.order_id == order.id) {
                order.amount -= refund.amount;
            }
        }
    }
    // int old = std::accumulate(orders.begin(), orders.end(), 0, SumAmount);
}
```
