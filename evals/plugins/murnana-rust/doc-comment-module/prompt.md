---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This is `src/rate_limit.rs` in our crate `throttle`. It has no doc comments at all and `#![warn(missing_docs)]` is complaining. Can you write the doc comments for it? Just reply with the full updated file.

```rust
use std::collections::VecDeque;

pub struct RateLimiter {
    max_calls: usize,
    per_seconds: f64,
    calls: VecDeque<f64>,
}

impl RateLimiter {
    pub fn new(max_calls: usize, per_seconds: f64) -> Self {
        assert!(max_calls > 0, "max_calls must be positive");
        Self { max_calls, per_seconds, calls: VecDeque::new() }
    }

    pub fn allow(&mut self, now: f64) -> bool {
        while let Some(&first) = self.calls.front() {
            if now - first < self.per_seconds {
                break;
            }
            self.calls.pop_front();
        }
        if self.calls.len() >= self.max_calls {
            return false;
        }
        self.calls.push_back(now);
        true
    }
}

pub fn parse_limit(spec: &str) -> Result<RateLimiter, String> {
    let (calls, seconds) = spec
        .split_once(':')
        .ok_or_else(|| format!("missing ':' in {spec:?}"))?;
    let calls: usize = calls.parse().map_err(|_| format!("bad call count in {spec:?}"))?;
    let seconds: f64 = seconds.parse().map_err(|_| format!("bad seconds in {spec:?}"))?;
    Ok(RateLimiter::new(calls, seconds))
}
```
