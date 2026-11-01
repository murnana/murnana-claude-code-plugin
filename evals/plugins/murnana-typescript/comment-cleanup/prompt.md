---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

コードレビューで「このファイルのコメントは整理したほうがいい」と言われました。コメントを見直して、整理後のコードと、各コメントをどう扱ったか（消した・移した・残した）を教えてください。

```ts
export function mergeOrders(orders: Order[], refunds: Refund[]): Order[] {
  // orders と refunds をループする
  for (const order of orders) {
    // #128 の修正 (2024-03): 返金が無いのに内側のループを回していたのでガードを追加
    if (refunds.length === 0) {
      continue;
    }
    for (const refund of refunds) {
      // refund の id が一致したら金額を引く
      if (refund.orderId === order.id) {
        order.amount -= refund.amount;
      }
    }
  }
  // const old = orders.reduce((sum, o) => sum + o.amount, 0);
  return orders;
}
```
