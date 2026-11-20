---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

マージする前に、このコードをレビューしてください。プロジェクトに決まったルールはありません。

```kotlin
import android.content.Context
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.io.File

object ThumbnailCache {
    lateinit var context: Context
    val entries = mutableMapOf<String, ByteArray>()
}

class GalleryActivity : android.app.Activity() {
    override fun onStart() {
        super.onStart()
        ThumbnailCache.context = this
        GlobalScope.launch {
            while (true) {
                val reader = File(filesDir, "index.txt").bufferedReader()
                val first = reader.readLine() ?: continue
                ThumbnailCache.entries[first] = File(filesDir, first).readBytes()
                reader.close()
                delay(1_000)
            }
        }
    }
}
```
