---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

マージする前に、このコードをレビューしてください。プロジェクトに決まったルールはありません。

```cpp
#include <cstdio>
#include <stdexcept>
#include <string>

class LogReader {
public:
    std::string ReadFirstLine(const std::string& path) {
        FILE* fp = std::fopen(path.c_str(), "r");
        if (fp == nullptr) {
            throw std::runtime_error("cannot open " + path);
        }
        char* buffer = new char[4096];
        if (std::fgets(buffer, 4096, fp) == nullptr) {
            throw std::runtime_error("empty file: " + path);
        }
        std::string line(buffer);
        delete buffer;
        std::fclose(fp);
        return line;
    }
};
```
