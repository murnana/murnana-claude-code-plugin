---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

このファイルの名前の付け方をレビューしてください。このプロジェクトには命名規則のルールがありません。

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
