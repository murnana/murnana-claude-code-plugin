---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

このコードの公開している部分に、使う人向けの説明（DocC comments）を書いてください。コードそのものは変えないでください。

```swift
import Foundation

let MAX_RETRY_COUNT = 3

protocol data_loading {
    func LoadData(from Url: URL) -> Data?
}

struct http_response {
    var StatusCode: Int
    var empty: Bool

    mutating func sorted_headers() {}
}

enum ConnectionState {
    case Idle
    case CONNECTED
}
```
