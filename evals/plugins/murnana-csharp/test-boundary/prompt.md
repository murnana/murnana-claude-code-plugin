---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

We have no tests for this C# function yet. Can you write the test cases for it? I can't run anything here, so just reply with the full test file.

```csharp
namespace Shop;

public static class Shipping
{
    /// <summary>Returns the shipping fee in yen for an order subtotal in yen.</summary>
    /// <remarks>Orders of 5000 yen or more ship free. Anything below costs 500 yen.</remarks>
    /// <exception cref="ArgumentOutOfRangeException"><paramref name="subtotal"/> is negative.</exception>
    public static int ShippingFee(int subtotal)
    {
        if (subtotal < 0)
        {
            throw new ArgumentOutOfRangeException(nameof(subtotal));
        }
        if (subtotal >= 5000)
        {
            return 0;
        }
        return 500;
    }
}
```
