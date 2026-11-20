---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

このコードの公開している部分に、使う人向けの説明（KDoc）を書いてください。コードそのものは変えないでください。

```kotlin
package com.Example.user_profile

const val maxNameLength = 40

class user_Repository {
    private val Cache = mutableMapOf<Int, String>()

    fun Load_User(UserId: Int): String? {
        val cached_name = Cache[UserId]
        return cached_name
    }
}

class XMLHTTPParser
```
