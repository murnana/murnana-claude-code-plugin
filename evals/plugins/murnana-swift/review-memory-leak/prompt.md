---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

マージする前に、このコードをレビューしてください。プロジェクトに決まったルールはありません。

```swift
import Foundation

protocol DownloadDelegate: AnyObject {
    func didFinish(_ data: Data)
}

final class Downloader {
    var delegate: DownloadDelegate?
    var onProgress: ((Double) -> Void)?
    private var timer: Timer?
    private var received = 0.0

    func start() {
        onProgress = { fraction in
            self.received = fraction
        }
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            self.onProgress?(self.received)
        }
    }

    deinit {
        timer?.invalidate()
    }
}
```
