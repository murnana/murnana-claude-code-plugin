---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This is `rate_limiter.h`. It has no doc comments at all and our Doxygen build is complaining. Can you write the doc comments for it? Just reply with the full updated header.

```cpp
#pragma once

#include <cstddef>
#include <deque>
#include <stdexcept>
#include <string>

namespace ratelimit {

class RateLimiter {
public:
    RateLimiter(std::size_t max_calls, double per_seconds)
        : max_calls_(max_calls), per_seconds_(per_seconds) {}

    bool Allow(double now) {
        while (!calls_.empty() && now - calls_.front() >= per_seconds_) {
            calls_.pop_front();
        }
        if (calls_.size() >= max_calls_) {
            return false;
        }
        calls_.push_back(now);
        return true;
    }

private:
    std::size_t max_calls_;
    double per_seconds_;
    std::deque<double> calls_;
};

inline RateLimiter ParseLimit(const std::string& spec) {
    const auto colon = spec.find(':');
    if (colon == std::string::npos) {
        throw std::invalid_argument("missing ':' in " + spec);
    }
    return RateLimiter(std::stoul(spec.substr(0, colon)), std::stod(spec.substr(colon + 1)));
}

}  // namespace ratelimit
```
