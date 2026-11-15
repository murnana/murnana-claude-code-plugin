---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

マージする前に、このコードをレビューしてください。プロジェクトに決まったルールはありません。

```typescript
import { useEffect, useState } from "react";

const responseCache = new Map<string, unknown>();

export function usePrice(symbol: string): number | undefined {
  const [price, setPrice] = useState<number>();

  useEffect(() => {
    const socket = new WebSocket(`wss://example.com/prices/${symbol}`);
    socket.addEventListener("message", (event) => {
      const data = JSON.parse(event.data);
      responseCache.set(`${symbol}:${Date.now()}`, data);
      setPrice(data.price);
    });
    const timer = setInterval(() => socket.send("ping"), 5_000);
    window.addEventListener("resize", () => setPrice((p) => p));
  }, [symbol]);

  return price;
}
```
