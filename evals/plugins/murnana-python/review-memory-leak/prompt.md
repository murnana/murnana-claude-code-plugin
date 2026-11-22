---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

マージする前に、このコードをレビューしてください。プロジェクトに決まったルールはありません。

```python
import functools
import json

_seen_requests = []


class ReportBuilder:
    def __init__(self, template_path):
        self.template = open(template_path).read()

    @functools.lru_cache(maxsize=None)
    def render(self, user_id):
        return self.template.replace("{user}", str(user_id))


def handle(request, builder):
    _seen_requests.append(request)
    log = open("/var/log/report.log", "a")
    payload = json.loads(request.body)
    log.write(builder.render(payload["user_id"]))
    log.close()
```
