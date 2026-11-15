---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

このファイルの名前の付け方をレビューしてください。このプロジェクトには命名規則のルールがありません。

```java
package com.Example.Billing;

import java.util.List;

public class invoice_printer {
    public static final int maxLines = 60;
    private String _customerName;
    private List<String> Lines;

    public void Print_Invoice(String CustomerName) {
        int line_count = Lines.size();
        System.out.println(CustomerName + ": " + line_count);
    }
}
```
