---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

このファイルの名前の付け方をレビューしてください。このプロジェクトには命名規則のルールがありません。

```rust
#![allow(nonstandard_style)]

pub const maxConnections: usize = 16;

pub struct HTTPClient {
    pub BaseUrl: String,
}

impl HTTPClient {
    pub fn get_base_url(&self) -> &str {
        &self.BaseUrl
    }

    pub fn SendRequest(&self, Path: &str) -> String {
        format!("{}{}", self.BaseUrl, Path)
    }

    pub fn to_bytes(&self) -> &[u8] {
        self.BaseUrl.as_bytes()
    }
}
```
