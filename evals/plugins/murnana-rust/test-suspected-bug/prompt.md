---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Please add tests for this Rust function so we can turn on the coverage gate. I can't run anything here, so reply with the full test file.

```rust
#[derive(Debug, PartialEq, Eq)]
pub enum ShippingError {
    NegativeSubtotal,
}

/// Returns the shipping fee in yen for an order subtotal in yen.
///
/// Orders of 5000 yen or more ship free. Anything below costs 500 yen.
///
/// # Errors
///
/// Returns [`ShippingError::NegativeSubtotal`] if `subtotal` is negative.
pub fn shipping_fee(subtotal: i64) -> Result<u32, ShippingError> {
    if subtotal < 0 {
        return Err(ShippingError::NegativeSubtotal);
    }
    if subtotal > 5000 {
        return Ok(0);
    }
    Ok(500)
}
```
