---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

このコードの公開している部分に、使う人向けの説明（docstrings）を書いてください。コードそのものは変えないでください。

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
