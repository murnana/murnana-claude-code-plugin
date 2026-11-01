---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our `Cargo.toml` has `rust-version = "1.65"`. A reviewer on my PR asked "why not just use `std::sync::OnceLock` instead of the `once_cell` crate here?" and I'd like the code to answer that question so the next reviewer doesn't ask again. Please add whatever comments this code needs and show me the updated code.

```rust
use once_cell::sync::OnceCell;

// a static cell for the config
static CONFIG: OnceCell<Config> = OnceCell::new();

pub fn config() -> &'static Config {
    // get the config or load it
    CONFIG.get_or_init(Config::load)
}
```
