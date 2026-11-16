---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

このコードの公開している部分に、使う人向けの説明（XML documentation comments）を書いてください。コードそのものは変えないでください。

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;

public interface orderRepository
{
    Task<Order> load_order(int OrderId);
}

public class order_service
{
    private readonly orderRepository Repository;
    private static int instanceCount;
    public const int MAX_ITEMS = 100;

    public async Task<Order> GetOrder(int OrderId)
    {
        var Result = await Repository.load_order(OrderId);
        return Result;
    }
}
```
