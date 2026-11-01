---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This module has no docstrings at all and our docs build is complaining. The project has no docstring style configured anywhere. Can you write the docstrings for it? Just reply with the full updated file.

```python
from collections.abc import Iterable


class RateLimiter:
    def __init__(self, max_calls: int, per_seconds: float) -> None:
        self.max_calls = max_calls
        self.per_seconds = per_seconds
        self._calls: list[float] = []

    def allow(self, now: float) -> bool:
        self._calls = [t for t in self._calls if now - t < self.per_seconds]
        if len(self._calls) >= self.max_calls:
            return False
        self._calls.append(now)
        return True


def parse_limits(lines: Iterable[str]) -> dict[str, RateLimiter]:
    limits = {}
    for line in lines:
        name, calls, seconds = line.split(":")
        if not calls.isdigit():
            raise ValueError(f"bad call count in {line!r}")
        limits[name] = RateLimiter(int(calls), float(seconds))
    return limits
```
