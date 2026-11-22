---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

We have no tests for this C++ function yet. Can you write the test cases for it? I can't run anything here, so just reply with the full test file.

```cpp
// shop/shipping.h
#pragma once

#include <stdexcept>

namespace shop {

/// Returns the shipping fee in yen for an order subtotal in yen.
///
/// Orders of 5000 yen or more ship free. Anything below costs 500 yen.
///
/// @throws std::invalid_argument if @p subtotal is negative.
inline int ShippingFee(int subtotal) {
  if (subtotal < 0) {
    throw std::invalid_argument("subtotal must not be negative");
  }
  if (subtotal >= 5000) {
    return 0;
  }
  return 500;
}

}  // namespace shop
```
