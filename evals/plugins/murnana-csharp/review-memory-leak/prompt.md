---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

マージする前に、このコードをレビューしてください。プロジェクトに決まったルールはありません。

```csharp
using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

public sealed class PriceWatcher
{
    private readonly PriceFeed _feed;
    private decimal _lastPrice;

    public PriceWatcher(PriceFeed feed)
    {
        _feed = feed;
        PriceFeed.GlobalPriceChanged += OnPriceChanged;
    }

    private void OnPriceChanged(object? sender, decimal price) => _lastPrice = price;

    public async Task SaveSnapshotAsync(string url, string path)
    {
        var client = new HttpClient();
        var response = await client.GetAsync(url);
        var file = new FileStream(path, FileMode.Create);
        await response.Content.CopyToAsync(file);
    }
}

public sealed class PriceFeed
{
    public static event EventHandler<decimal>? GlobalPriceChanged;
}
```
