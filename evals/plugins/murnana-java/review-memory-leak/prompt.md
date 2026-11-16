---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

マージする前に、このコードをレビューしてください。プロジェクトに決まったルールはありません。

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class AuditLog {
    private static final List<String> HISTORY = new ArrayList<>();

    public String readHeader(String path) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(path));
        String header = reader.readLine();
        if (header == null) {
            throw new IOException("empty file: " + path);
        }
        HISTORY.add(header);
        reader.close();
        return header;
    }
}
```
