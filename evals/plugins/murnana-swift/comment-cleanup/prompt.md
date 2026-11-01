---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

コードレビューで「このファイルのコメントは整理したほうがいい」と言われました。コメントを見直して、整理後のコードと、各コメントをどう扱ったか（消した・移した・残した）を教えてください。

```swift
func mergeOrders(_ orders: [Order], refunds: [Refund]) -> [Order] {
    var orders = orders
    // orders と refunds をループする
    for index in orders.indices {
        // #128 の修正 (2024-03): 返金が無いのに内側のループを回していたのでガードを追加
        if refunds.isEmpty {
            continue
        }
        for refund in refunds {
            // refund の id が一致したら金額を引く
            if refund.orderID == orders[index].id {
                orders[index].amount -= refund.amount
            }
        }
    }
    // let old = orders.reduce(0) { $0 + $1.amount }
    return orders
}
```
