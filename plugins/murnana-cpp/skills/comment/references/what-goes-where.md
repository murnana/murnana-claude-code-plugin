# What goes where

How to decide whether a piece of information belongs in a C++ comment, and how to write it when it does. Read this before writing, keeping or deleting any implementation comment.

## Contents

- The rule
- Deciding about one comment
- "Why not" comments
- "Why" comments that stay in the code
- Constants
- TODO and FIXME
- Comments to remove
- Style

## The rule

"Code says How, tests say What, the commit log says Why, and code comments say Why not." The rule comes from Takuto Wada (t_wada, https://x.com/t_wada/status/904916106153828352, 2017). He later explained that "why not" means "why another way was not taken": what was deliberately *not* done can't be seen in the code, so a comment is the only place for it.

Treat it as a mnemonic, not a law. Two additions, both widely argued (John Ousterhout, *A Philosophy of Software Design*; the Stack Overflow Blog's comment guidelines):

- A Why that every future editor of the line must know belongs in the code too, even if the commit message also has it. Readers rarely search the log, and the commit that explains a line is often not the latest one touching it.
- API documentation (Doxygen doc comments) is a separate category. It states the contract for callers: the "What" from their side. "Comments only say why not" applies to implementation comments, not to the API documentation.

## Deciding about one comment

Ask in order. The first "yes" decides.

1. Does it describe the contract of a public or protected declaration? → Doc comment on the declaration.
2. Could a better name, an extracted function, or an explaining variable say it? → Change the code (or propose it), drop the comment.
3. Is it a behavior that should never regress? → A test. The comment may stay only as part of a doc comment's contract.
4. Is it about the change (why it was made, what it replaced, who asked)? → Commit message. For a change you are making now, suggest the line for the commit message; for an old change, just delete the comment.
5. Does it record an alternative that was rejected, a workaround, or a constraint not visible in the code? → Keep it as a "why not" comment.
6. Would someone editing this line break something without knowing it? → Keep it as a "why" comment.
7. Otherwise → delete it.

## "Why not" comments

A complete one has three parts:

1. **The alternative** a reader would reach for.
2. **The reason** it wasn't taken: a constraint, a measurement, a spec, a bug link.
3. **The revisit condition**: when the reason stops holding.

The third part makes the comment safe to delete later. Without it, nobody dares to remove it.

Keeps a seemingly worse container:

```cpp
// std::map, not std::unordered_map: the report is diffed against golden
// files, so iteration order must be stable across platforms.
std::map<std::string, Totals> totals_by_region;
```

Deliberately not optimized (with the measurement):

```cpp
// Linear search instead of a hash index: the table holds at most 32
// entries (kMaxPlugins) and a lookup took ~40 ns in bench/lookup.cpp.
// Revisit if kMaxPlugins grows past a few hundred.
auto it = std::find_if(plugins.begin(), plugins.end(), matches_id);
```

A workaround for a language or toolchain limit:

```cpp
// Not a structured binding: a lambda can't capture one before C++20,
// and this target still builds as C++17. Use `auto& [key, value]`
// once the project moves to C++20.
const auto& key = entry.first;
```

A rejected refactoring (so the next person doesn't repeat it):

```cpp
// Kept as a switch. Replacing it with virtual dispatch was tried in #482:
// the handlers must run in declaration order, which a vtable can't express
// without a separate ordering table.
switch (event.kind) {
```

A non-idiomatic choice:

```cpp
// std::memcpy, not reinterpret_cast: reading a float through a uint32_t
// pointer breaks strict aliasing. Switch to std::bit_cast when the
// project moves to C++20.
std::uint32_t bits;
std::memcpy(&bits, &value, sizeof bits);
```

## "Why" comments that stay in the code

Keep a Why in the code when breaking it is easy and the breakage is silent:

```cpp
// Lock order: registry_mutex_ before entry.mutex. Reversing it deadlocks
// with Registry::compact().
std::scoped_lock lock(registry_mutex_, entry.mutex);
```

```cpp
// RFC 4180 requires CRLF line endings, even on POSIX.
out << "\r\n";
```

```cpp
// Must run before the first allocation: the custom allocator reads
// this flag only once, at startup.
set_allocator_debug(true);
```

Link the spec, the issue, or the benchmark rather than paraphrasing it at length. A link plus one sentence of the conclusion is enough.

## Constants

Name the constant, then say where the value comes from if the name can't:

```cpp
// Upper bound from the device datasheet, section 7.3 (max burst length).
constexpr std::size_t kMaxBurstBytes = 4096;
```

Don't explain a value the name already explains (`constexpr int kSecondsPerMinute = 60;` needs nothing).

## TODO and FIXME

- Format: `// TODO(<issue>): <what>, <when>` and `// FIXME(<issue>): <known defect>`. The issue reference is what makes it tracked work instead of a wish. Follow the project's own format if it has one (for example `TODO(name)` or `TODO(bug 123)`).
- Give a concrete trigger ("once the minimum compiler supports C++20", "when #512 lands"), not "later" or "someday".
- A TODO reserves future work; a "why not" records a decision. Don't write a TODO for something that was decided against. Write the "why not".
- Doxygen's `@todo` puts the item on a generated Todo list. Use it only inside a doc comment, for a gap in the API that users should know about. Use `// TODO` for implementation work.

## Comments to remove

| Pattern | Example | Instead |
|---|---|---|
| Restates the code | `++retries; // increment retries` | Nothing |
| Compensates for a name | `int d; // elapsed time in days` | `int elapsed_days;` |
| Narrates the steps (How) | `// loop over items and sum prices` | Extract `total_price(items)` |
| Change log in the file | `// 2024-03-02 tanaka: fixed overflow` | Delete; version control has it |
| Why of the change | `// Changed to int64 because of #88` | Delete; the commit that made the change records it. If the 64-bit width is an invariant, rewrite as that instead: `// int64: totals exceed 2^31 for yearly reports` |
| Commented-out code | `// old_impl(x);` | Delete; version control keeps it |
| Closing-brace labels on blocks | `} // end if` | Delete. Keep `}  // namespace foo`, which is conventional |
| Misleading or cryptic | `// magic, don't touch` | Find the real reason or ask; otherwise delete |

## Style

- Write the conclusion first, in one or two short sentences. Add a link for the details.
- Use the present tense for facts about the code ("must run before…"), the past tense for events ("was tried in #482").
- Write it so a later reader can delete it confidently: name the premise it depends on.
- Place the comment directly above the line it explains, not at the end of a long line.
