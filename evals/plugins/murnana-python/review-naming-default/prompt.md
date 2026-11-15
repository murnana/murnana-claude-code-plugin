---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

このファイルの名前の付け方をレビューしてください。このプロジェクトには命名規則のルールがありません。

```python
maxRetries = 3


class http_client:
    def __init__(self, BaseUrl):
        self.BaseUrl = BaseUrl
        self.requestCount = 0

    def SendRequest(self, Path):
        fullUrl = self.BaseUrl + Path
        self.requestCount += 1
        return fullUrl


class ConnectionFailed(Exception):
    pass
```
