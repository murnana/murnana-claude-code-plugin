# Field notes

Practical lessons for commenting Kotlin, written by Claude from experience. They are not from the cited sources; where they conflict with comment-roles.md or kdoc.md, those win.

## Working order

- **Delete first, then write.** Clear How comments, commented-out code and stale notes before adding anything; what remains shows where a real gap is. A good pass often removes more lines than it adds.
- **One file or one class per pass.** Large comment diffs get skimmed, and a wrong comment slips through review. For a whole module, do the public API first, then implementation comments.
- **Keep comment edits out of code commits.** A comment-only diff is easy to review. Suggest the user commit it separately from any rename or refactor that follows from the report.
- **Before deleting, check history once.** A comment that looks like How (`// use toList() here`) may be a terse Why not. If `git log -L` / `git blame` shows it was added with a fix, rewrite it as a proper Why-not comment instead of deleting it.
- **Unsure whether a comment is still true?** Don't delete it and don't "fix" it. List it in the report.

## Project rules come first

- Check `.editorconfig`, ktlint and detekt configs (`detekt.yml`: `UndocumentedPublicClass`, `UndocumentedPublicFunction`, `CommentOverPrivateFunction`, and similar). If detekt requires KDoc on every public function, that overrides "skip KDoc when the name says it all": write the shortest contract-only sentence.
- Wrap KDoc at the project's max line length (`max_line_length` in `.editorconfig`; ktlint's default depends on its code style, e.g. 140 for `ktlint_official`, 100 for `android_studio`). Wrap at sentence or clause boundaries, not mid-link.
- Don't reformat surrounding code. Touch only comment lines and blank lines around them.

## Kotlin-specific things worth documenting

The type system already says a lot. KDoc earns its place by saying what the types can't:

| Construct | Say in KDoc | Don't say |
|---|---|---|
| Nullable return `T?` | What `null` means: "not found", "not loaded yet", "cancelled". | "Returns null if null". |
| `require` / `check` / `error()` in the body | The precondition in prose, plus `@throws IllegalArgumentException` / `IllegalStateException` when callers might hit it. | The exact check expression. |
| `suspend fun` | Whether it is main-safe, what happens on cancellation (partial writes? rollback?), and whether it can suspend for long (network). | "This is a suspend function". |
| `Flow` / `StateFlow` / `SharedFlow` | Cold or hot, whether it completes, what it emits first (replay, initial value), on which dispatcher it emits if not the collector's. | The operator chain that builds it. |
| Classes with mutable state | Thread-safety: "not thread-safe", "safe to call from any thread", "confined to the main thread". | Locking details. |
| Numeric time or size params | The unit (ms, s, bytes, px vs dp). Better: propose `kotlin.time.Duration` or a value class in the report. | — |
| `sealed` hierarchies | Each subclass documents its own meaning at its declaration. The parent says what the hierarchy models. | A list of subclasses in the parent: it rots when one is added. |
| `data class` / `value class` | Constructor properties via `@property`, with constraints (range, format) that the type doesn't enforce. | "Data class holding X". |
| `companion object` factory (`of`, `from`, `create`) | How it differs from the constructor (validation, caching, normalization). | — |
| `@JvmOverloads`, `@JvmStatic`, `@JvmName` | Nothing usually. Mention Java callers only when the Java view behaves differently. | — |
| `internal` in a library | Optional. Not public API; treat it like implementation. | — |

## Constructs that almost always need a Why-not comment

- `@Suppress("...")`: why the warning is wrong here. A bare suppression looks like hiding a bug.
- `!!`: why it can't be null at this point. Better: propose `checkNotNull(x) { "reason" }` or `requireNotNull`, whose message carries the reason and needs no comment.
- `@OptIn(...)` / experimental API: why relying on it is acceptable, and what to watch when upgrading.
- `runBlocking`, `GlobalScope`, `Dispatchers.Unconfined`, `lateinit` on a public property, `Any` / unchecked casts: name the safer alternative and why it doesn't fit.
- Catching `Exception` / `Throwable`, or swallowing `CancellationException`: why the broad catch is right (and that cancellation is rethrown).
- An empty `else -> {}` / empty `catch`: why doing nothing is correct.
- Magic numbers: first propose a named `const val`. If the value comes from an outside source (a spec, a server limit), the constant's KDoc or a comment links to it.

## Phrasing

- KDoc in Japanese: write the summary in plain form, ending with 「。」: 「指定した [id] のユーザーを返す。」. Use one style per codebase (plain だ・である form or polite です・ます form, never mixed). Keep code identifiers and `[links]` as is; don't translate them.
- KDoc in English: third person, present tense: "Returns…", not "Return…" or "This function returns…".
- Start with the result or effect, not with "This function", "This class", "Helper to", "Utility for".
- Don't restate the name: `getUser(id)` → not "Gets the user". Say what the name can't: "Returns the cached user for [id], fetching from the server if the cache is older than 5 minutes."
- No marketing or filler words: "efficiently", "robust", "simply", "just", "basically", "Note:", emojis.
- One fact per sentence. If a KDoc grows past ~5 lines, the declaration may be doing too much. Say so in the report instead of writing a longer comment.

## Comments generated by AI tools (including this skill)

Typical over-commenting to look for and remove:

- A comment above every line or block, narrating the code.
- KDoc on private helpers and on overrides that only repeat the parent.
- `@param` / `@return` for every parameter, each repeating the parameter name.
- "Why" comments that sound plausible but have no source. Treat them as unverified. Check them against history, or ask the user.

## Checks the user can run afterwards

Suggest these in the report when the project has them; don't run build tools unasked:

- `./gradlew detekt` or `./gradlew ktlintCheck`: style and documentation rules.
- `./gradlew dokkaGenerate` (Dokka 2) or `./gradlew dokkaHtml` (Dokka 1): renders the KDoc and warns about unresolved links.
