---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

このファイルの名前の付け方をレビューしてください。このプロジェクトには命名規則のルールがありません。

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
