# KDoc reference

Sources (summarized and adapted by Claude; not the original text):

- "Document Kotlin code: KDoc" — https://kotlinlang.org/docs/kotlin-doc.html
- "Coding conventions: Documentation comments" — https://kotlinlang.org/docs/coding-conventions.html#documentation-comments
- "Module and package documentation" — https://kotlinlang.org/docs/dokka-module-and-package-docs.html

Source files: https://github.com/JetBrains/kotlin-web-site (`docs/topics/`), Apache License 2.0. See `THIRD_PARTY_NOTICES.md` at the plugin root.

## Shape

- A KDoc comment opens with `/**` and closes with `*/`. Leading `*` on each line is not part of the text.
- Multi-line: `/**` on its own line, each following line starts with ` * `.
- Short: one line, `/** Returns the cached value, or `null` if expired. */`.
- First paragraph (up to the first blank line) is the summary shown in lists; the rest is the detailed description.
- Each block tag starts a new line with `@`.
- Inline formatting is Markdown.

```kotlin
/**
 * A group of *members*.
 *
 * This class has no useful logic; it's just a documentation example.
 *
 * @param T the type of a member in this group.
 * @property name the name of this group.
 * @constructor Creates an empty group.
 */
class Group<T>(val name: String) {
    /**
     * Adds a [member] to this group and returns the new size of the group.
     */
    fun add(member: T): Int { /* ... */ }
}
```

## Parameters and return values: prefer prose

The coding conventions advise against `@param` / `@return` in general. Describe them in the text and link parameters with `[name]`. Use the tags only for a description too long to fit the main text.

```kotlin
// Avoid
/**
 * Returns the absolute value of the given number.
 * @param number The number to return the absolute value for.
 * @return The absolute value.
 */
fun abs(number: Int): Int

// Prefer
/** Returns the absolute value of the given [number]. */
fun abs(number: Int): Int
```

## Block tags

| Tag | Use for |
|---|---|
| `@param name` | A value parameter of a function, or a type parameter of a class, property or function. `@param[name]` is equivalent. |
| `@return` | The return value of a function. |
| `@constructor` | The primary constructor of a class. |
| `@receiver` | The receiver of an extension function. |
| `@property name` | A property of a class, mainly one declared in the primary constructor (where a comment before the declaration would be awkward). |
| `@throws Class` / `@exception Class` | An exception the method may throw. Kotlin has no checked exceptions, so this is optional; document the ones callers should know about. |
| `@sample identifier` | Embeds the body of the named function as a usage example. |
| `@see identifier` | Adds a link in the "See also" block. |
| `@author` | The author of the element. Usually leave it out: git records authorship. |
| `@since` | The software version in which the element was introduced. |
| `@suppress` | Hides the element from generated docs, for things that must be public but are not official API. |

There is no `@deprecated` tag. Deprecation is the annotation below; adding it is a code change, so the skill proposes it in the report instead of writing it:

```kotlin
@Deprecated("Use fetchAll()", ReplaceWith("fetchAll()"))
fun fetch(): List<Item>
```

## Links

- Element link: `[foo]`. Custom label: `[this method][foo]`.
- Qualified names always use dots, also before a member name (unlike Javadoc's `#`): `[kotlin.reflect.KClass.properties]`.
- Names resolve as if written inside the documented element, so imported names need no qualification.
- There is no syntax to pick one overload; a link to a function covers all its overloads (they share one doc page).
- External links use normal Markdown: `[KDoc](https://kotlinlang.org/docs/kotlin-doc.html)`.

## What to document

- Libraries: KDoc on every public member, except overrides that add nothing new.
- Applications: the public API other modules use. Private members only when they hold a Why not (use `//`, see comment-roles.md).

## Module and package documentation (Dokka)

Module and package docs live in a separate Markdown file passed to Dokka through its `includes` option (Gradle, Maven or CLI configuration).

- `# Module <module name>` starts the module section.
- `# Package <fully qualified package name>` starts a package section.
- Everything until the next level-1 heading belongs to that section; `##`–`######` headings stay inside it.
- One file may hold both kinds, or use one file per module or package.

```markdown
# Module kotlin-demo
Shown under the module name.

# Package org.jetbrains.kotlin.demo
Shown in the package list and on the package page.

## Details
Still part of org.jetbrains.kotlin.demo.
```

Before adding such a file, check the build already passes one via `includes`; if not, tell the user the build setting is needed rather than editing the build unasked.
