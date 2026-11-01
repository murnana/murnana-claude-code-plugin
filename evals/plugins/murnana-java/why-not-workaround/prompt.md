---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our `pom.xml` sets `<maven.compiler.source>1.8</maven.compiler.source>` and `<maven.compiler.target>1.8</maven.compiler.target>`. A reviewer on my PR asked "why not just use `nickname.isEmpty()` here?" and I'd like the code to answer that question so the next reviewer doesn't ask again. Please add whatever comments this method needs and show me the updated code.

```java
static String displayName(Optional<String> nickname, String fullName) {
    // check if the nickname is missing
    if (!nickname.isPresent()) {
        // use the full name
        return fullName;
    }
    return nickname.get();
}
```
