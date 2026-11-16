---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

このコードの公開している部分に、使う人向けの説明（Javadoc）を書いてください。コードそのものは変えないでください。

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
