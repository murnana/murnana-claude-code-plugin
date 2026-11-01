---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

コードレビューで「このファイルのコメントは整理したほうがいい」と言われました。コメントを見直して、整理後のコードと、各コメントをどう扱ったか（消した・移した・残した）を教えてください。

```java
static List<Order> mergeOrders(List<Order> orders, List<Refund> refunds) {
    // orders と refunds をループする
    for (Order order : orders) {
        // #128 の修正 (2024-03): 返金が無いのに内側のループを回していたのでガードを追加
        if (refunds.isEmpty()) {
            continue;
        }
        for (Refund refund : refunds) {
            // refund の id が一致したら金額を引く
            if (refund.orderId() == order.id()) {
                order.subtractAmount(refund.amount());
            }
        }
    }
    // int old = orders.stream().mapToInt(Order::amount).sum();
    return orders;
}
```
