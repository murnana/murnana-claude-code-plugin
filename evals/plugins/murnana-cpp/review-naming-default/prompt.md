---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

このファイルの名前の付け方をレビューしてください。このプロジェクトには命名規則のルールがありません。

```cpp
#include <string>
#include <vector>

#define maxRetry 3

class HTTP_Client {
public:
    int SendRequest(const std::string& strUrl);

private:
    int m_iTimeout = 30;
    std::vector<std::string> Headers;
};

enum class connection_state { IDLE, CONNECTED };
```
