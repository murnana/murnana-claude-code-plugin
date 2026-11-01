---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our `CMakeLists.txt` has `set(CMAKE_CXX_STANDARD 17)`. A reviewer on my PR asked "why not just use `std::format` here?" and I'd like the code to answer that question so the next reviewer doesn't ask again. Please add whatever comments this function needs and show me the updated code.

```cpp
#include <iomanip>
#include <sstream>
#include <string>

std::string FormatPrice(const std::string& currency, double amount) {
    // build the message
    std::ostringstream out;
    out << currency << ' ' << std::fixed << std::setprecision(2) << amount;
    // return the string
    return out.str();
}
```
