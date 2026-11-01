# Comment roles: How / What / Why / Why not

Source: Takuto Wada (@t_wada), post on X, 2017-09-05 (JST) — https://x.com/t_wada/status/904916106153828352

> コードには How テストコードには What コミットログには Why コードコメントには Why not を書こうという話をした

In a reply the same day, t_wada confirmed that "Why not" means why another approach was not taken: the things deliberately *not* done are what to leave in code comments, for later readers and for oneself. Code can only show what was done; what was deliberately not done has no place to live except a comment.

The guidance below is Claude's own explanation of that principle applied to Kotlin; it is not t_wada's text.

## The split

| Place | Carries | Lives as long as | Read by |
|---|---|---|---|
| Code | **How**: the steps, made readable by names and structure | the code | everyone who reads the line |
| Test code | **What**: the behavior the code promises, as executable examples | the behavior | people changing the behavior |
| Commit log | **Why**: the reason for this change at this time | forever, tied to the diff | people asking "why did this change?" (`git blame`, `git log -L`) |
| Code comment | **Why not**: the obvious alternative that was rejected, and why | the code next to it | people about to "simplify" the code |

Each piece of information has one home. A comment that duplicates another home rots: the code changes, the comment doesn't, and the comment starts to lie.

Treat the split as a mnemonic, not a law. t_wada called the four-way mapping a bit forced, and later wrote of leaving "Why and Why not in the commit log or code comments" for an unavoidable workaround. Two refinements follow (see "Why → commit message" and "KDoc is a separate track").

## How → fix the code, not the comment

A comment explaining what the next lines do is a request for better code: a better name, an extracted function, an explaining variable or a named constant.

```kotlin
// Before
// filter out users who haven't logged in for 90 days
val result = users.filter { it.lastLogin > now.minus(90, DAYS) }

// After: the name says it, no comment needed
val activeUsers = users.filter { it.isActiveAt(now) }
```

Propose the rename or extraction; don't apply behavior-preserving refactors unless asked.

Exception: code that cannot be made self-explaining (a regular expression, a bit trick, a non-trivial algorithm) may carry a short comment on what it matches or computes.

## What → tests

Inside a function body, a comment saying what the result should be belongs in a test. Name tests so they read as the specification:

```kotlin
@Test
fun `returns empty list when no user logged in within 90 days`() { /* ... */ }
```

## KDoc is a separate track

The How/What/Why/Why-not split is about **implementation comments** (`//` inside and around bodies). KDoc on a public declaration is the **API contract**: the What for callers who never read the tests or the body. Don't apply "comments carry only Why not" to KDoc.

Keep KDoc to what callers may rely on (inputs, result, errors, threading, what `null` means), never implementation steps, so the body can change without the doc becoming false.

## Why → commit message (with one exception)

"Changed to X because the vendor API started rate-limiting" is history. Put it in the commit message body, where `git blame` finds it next to the exact diff: summary on the first line, the reason after a blank line. "Applied review feedback" is not a reason; write why the change was needed.

When the reason for a change is not in history, draft a commit message for the user instead of adding a comment.

Exception: a reason that **anyone touching this line must know to read it correctly** also goes in a comment, even if it duplicates the commit message. People reading code rarely go to the log, the relevant commit is often not the latest one for that line, and commit messages tend to be short. Test: if the line were changed without knowing the reason, would it break? Then it belongs next to the code. Usually such a reason is in fact a Why not.

## Why not → code comment

Write a comment when a competent reader would try the obvious alternative and break something, or waste time rediscovering that it fails. Typical cases:

- a simpler-looking expression that is wrong for a non-obvious reason;
- an optimization deliberately not done, because the data is small;
- a newer or more idiomatic API not used, because of a platform or environment limit;
- a workaround for an external bug or an unexpected spec;
- a refactoring that was tried and abandoned, so the next person doesn't repeat it;
- a value or format fixed by an external spec (link the spec).

```kotlin
// Not `list.sortedBy { it.priority }`: the server sends ties in random
// order, so ties are also ordered by id to keep the UI from reordering on
// every refresh.
val ordered = list.sortedWith(compareBy({ it.priority }, { it.id }))

// Not `runBlocking`: this runs on the main thread during startup, and
// blocking here triggers ANR on slow devices. See #1234.
scope.launch { warmUpCache() }

// Not `HashMap`: iteration order is part of the exported JSON format.
private val fields = LinkedHashMap<String, Field>()

// Linear search, not an index: at most ~30 entries per screen.
// Revisit if a screen can exceed a few hundred.
fun find(id: String) = entries.firstOrNull { it.id == id }

// Kept as a `when`, not a sealed-class hierarchy: plugins add cases at
// runtime, which a sealed hierarchy cannot express (tried in #872).
```

Good Why-not comments:

1. name a concrete alternative (`runBlocking`, `HashMap`, "an index", "a sealed hierarchy");
2. give a checkable reason (a bug or issue link, a spec section, a measured cost, a platform limit);
3. state, when there is one, the condition under which the reason stops holding ("revisit if…"), so a later reader can safely delete the comment and the code together;
4. sit right next to the code they protect.

Bad ones: "don't touch this", "this is tricky", "workaround" with no reason, or a guessed reason. If the reason cannot be confirmed from code, history or the user, leave no comment and report the spot.

## TODO and FIXME

A TODO reserves future work; a Why not records a decision not to do something. Keep them apart.

- Write `TODO(#123): …` or `FIXME(#123): …` with an issue reference (or owner), and a concrete trigger ("after the v2 API ships") instead of "someday".
- Kotlin's `TODO()` function throws at runtime; it is not a comment. Don't add it in place of a comment.
- A bare TODO with no owner, issue or condition: don't delete it silently; list it in the report so the user can file an issue or drop it.

## Other comments to remove

- Commented-out code (git keeps it).
- Change logs, author and date notes (git records them).
- Comments that no longer match the code. Report these: the mismatch may be a bug in the code, not in the comment.

## See also

- John Ousterhout, *A Philosophy of Software Design*, ch. 13 and 16.3 (comments for what isn't obvious; comments belong in the code, not the commit log).
- Ellen Spertus, "Best practices for writing code comments", Stack Overflow Blog, 2021 — https://stackoverflow.blog/2021/12/23/best-practices-for-writing-code-comments/
- Hillel Wayne, "Why Not Comments" (newsletter), 2024-09-10.
- Google Engineering Practices, "What to look for in a code review: Comments" — https://google.github.io/eng-practices/review/reviewer/looking-for.html#comments
