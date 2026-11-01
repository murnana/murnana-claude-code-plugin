---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

コードレビューで「このファイルのコメントは整理したほうがいい」と言われました。コメントを見直して、整理後のコードと、各コメントをどう扱ったか（消した・移した・残した）を教えてください。

```csharp
public static List<Order> MergeOrders(List<Order> orders, List<Refund> refunds)
{
    // orders と refunds をループする
    foreach (var order in orders)
    {
        // #128 の修正 (2024-03): 返金が無いのに内側のループを回していたのでガードを追加
        if (refunds.Count == 0)
        {
            continue;
        }
        foreach (var refund in refunds)
        {
            // refund の id が一致したら金額を引く
            if (refund.OrderId == order.Id)
            {
                order.Amount -= refund.Amount;
            }
        }
    }
    // var old = orders.Sum(o => o.Amount);
    return orders;
}
```
