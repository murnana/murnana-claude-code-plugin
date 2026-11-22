---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

このコードの公開している部分に、使う人向けの説明（Doxygen comments）を書いてください。コードそのものは変えないでください。

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
