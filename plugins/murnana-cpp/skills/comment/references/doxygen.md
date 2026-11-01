# Doxygen for C++

How to write Doxygen doc comments in C++ that render as intended, and how to check them. Summarized in our own words from the Doxygen manual (https://www.doxygen.nl/manual/, sources at https://github.com/doxygen/doxygen/tree/master/doc). Behaviors marked "verified" were checked with Doxygen 1.9.8 and clang 18. When this file and the manual disagree, the manual wins.

## Contents

- Comment block forms
- Brief and detailed descriptions
- Where the block goes
- Files and namespaces must be documented
- Commands to use
- Overloads, overrides and repeated docs
- Markdown and autolink pitfalls
- A complete example
- Validation

## Comment block forms

Doxygen reads these as doc comments in C++. Use the project's choice; the default for this skill is `///` with `@` commands.

| Form | Example |
|---|---|
| C++ line, triple slash | `/// text` |
| C++ line, Qt style | `//! text` |
| Javadoc block | `/** text */` |
| Qt block | `/*! text */` |
| After a member | `///<`, `//!<`, `/**<`, `/*!<` |

- Every command can start with `\` or `@`. They're interchangeable; keep one per project.
- A blank line ends a `///` block. To separate the brief from the details inside one block, use an empty `///` line.
- In `/** */` blocks, the leading `*` on each line is optional and stripped.

## Brief and detailed descriptions

Each entity has an optional brief (one line, shown in member lists and tooltips) and an optional detailed description.

- A **single** `///` line is a brief description.
- A `///` block of **two or more lines** is a detailed description, with an **empty brief**, unless the project sets `MULTILINE_CPP_IS_BRIEF` or `JAVADOC_AUTOBRIEF` to `YES` (both default to `NO`). Verified: the member list then shows no summary.
- So start every multi-line block with `@brief`. `@brief` ends at the first blank line (an empty `///`) or the next section command such as `@param`.
- With `JAVADOC_AUTOBRIEF = YES`, the first sentence (up to `.`, `?` or `!` followed by a space or newline) becomes the brief, for both `/**` and `///` blocks. To keep a period inside that sentence from ending it, write a backslash and a space after it (`e.g.\ only`).
- Several briefs or detailed blocks for one entity are joined in an unspecified order. Write one block per entity.

## Where the block goes

- Directly before the declaration. Doxygen also accepts it before the definition, but this skill puts API docs on the header declaration only.
- `///<` after a member documents that member, on the same line. Use it for enumerators and data members. It can't document a class, struct, union, enum, namespace, file or macro itself, and structural commands aren't allowed inside it. It also works on function parameters (`int v ///< [in] ...`), but prefer `@param`.
- `///` or `/** */` **inside a function body** becomes the function's "in-body" documentation and is appended to its API docs (verified). Use `//` in bodies.
- Structural commands (`@class`, `@fn`, `@var`, `@struct`, `@enum`, `@def`, `@namespace`) are needed only when the block is away from the entity. Before the entity they are redundant, duplicate the signature, and break when the signature changes. Don't add them there.

## Files and namespaces must be documented

- A global function, variable, typedef, enum or macro appears in the output only if its file is documented (or `EXTRACT_ALL = YES`). A header with any of those needs a block containing `@file` (an empty `@file` means "this file").
- Likewise, members of a namespace appear only if the namespace is documented somewhere, and members of a class only if the class is.
- Verified: in both cases Doxygen prints **no warning**; the entities are just missing from the HTML pages (they appear only in the source listing).

```cpp
/// @file
/// @brief Geometry primitives shared by the renderer and the physics code.
```

```cpp
/// @brief Geometry primitives and the operations on them.
namespace geo {
```

Document a namespace once (in its main header), not in every file that reopens it.

## Commands to use

Arguments: `<word>` takes one word, `(line)` takes the rest of the line, `{paragraph}` runs until a blank line or the next section command.

| Command | Use for |
|---|---|
| `@brief {text}` | One-sentence summary |
| `@details {text}` | Explicit start of the detailed part (optional; text after the empty `///` line is detailed anyway) |
| `@param[dir] <name> {text}` | One parameter. `dir` is `[in]`, `[out]` or `[in,out]`. The name must match the signature: a mismatch is warned. An unnamed parameter can be referred to by position, starting at 1 |
| `@tparam <name> {text}` | One template parameter |
| `@return {text}` / `@returns` | The return value. Not for `void` functions or constructors |
| `@retval <value> {text}` | A specific return value (`nullptr`, `false`, `-1`) |
| `@throws <type> {text}` | An exception and when it's thrown (synonyms `@throw`, `@exception`). The type isn't checked |
| `@pre {text}` / `@post {text}` | Precondition / postcondition |
| `@invariant {text}` | Class invariant |
| `@note {text}` | Side information worth highlighting |
| `@warning {text}` | Misuse with serious consequences (undefined behavior, data loss) |
| `@deprecated {text}` | Deprecation, with the replacement. Also adds the entity to the Deprecated list |
| `@since {text}` | Version that introduced the entity |
| `@sa {refs}` / `@see` | Related entities |
| `@todo {text}` | Known API gap; also adds to the Todo list |
| `@code{.cpp}` … `@endcode` | Usage example; documented names become links |
| `@snippet <file> <id>` | Example quoted from a compiled file between `//! [id]` markers (needs `EXAMPLE_PATH`) |
| `@p <word>` | Refer to a parameter in running text |
| `@c <word>` | One word in code font (use backticks for longer spans) |
| `@ref <name> ["text"]` | Explicit link, e.g. to a lowercase symbol autolink won't catch |
| `@copydoc <entity>` | Copy another entity's docs. For overloads, give argument types without spaces: `@copydoc parse(const char*,std::size_t)` |
| `@copybrief` / `@copydetails` | Copy only the brief / the detailed part |
| `@overload` | Standard "overloaded member function" text for a convenience overload |
| `@internal` … `@endinternal` | Text shown only with `INTERNAL_DOCS = YES` |
| `@cond [label]` … `@endcond` | Exclude a region from processing (unless `label` is in `ENABLED_SECTIONS`) |
| `@name (title)` + `@{` … `@}` | Group members under a heading inside a class |
| `@defgroup`, `@ingroup`, `@addtogroup` | Module pages across files |

Multiple adjacent `@param`, `@retval`, `@pre`, `@note` and so on are joined into one paragraph, each item on its own line. Keep them adjacent.

Unknown commands (`@parma`) are reported as warnings by both Doxygen and clang.

## Overloads, overrides and repeated docs

- An override inherits the base documentation by default (`INHERIT_DOCS = YES`; verified). Write a block only for what it adds or narrows.
- A convenience overload: `@overload` plus what differs. For a family with the same contract, document one and `@copydoc` it in the rest.
- `@copydoc` needs the source's enclosing class, file or namespace to be documented too.

## Markdown and autolink pitfalls

Markdown is on by default inside doc comments.

- **Indentation**: a line indented 4 or more spaces relative to the previous paragraph becomes a code block. Don't indent continuation lines of a paragraph; use `@code` for code.
- **Lists in `/** */` blocks**: Doxygen strips leading `*` before parsing, so a `*` list item without the column of lineup stars disappears. Use `-` for list items.
- **Code spans**: a single quote inside a backtick span cancels it (`` `don't` `` doesn't render as code). Use double backticks around a span that contains a quote.
- **Emphasis**: `*`/`_` start emphasis only before an alphanumeric and after whitespace or `<{([,:;`. `snake_case_names` are left alone.
- **Autolink**: words matching documented classes (with at least one uppercase letter), `func()`, `Class::member` and words with a dot inside (file names) become links. Put `%` before a word to stop it (`%Buffer` in prose about the concept, not the class). Use `@ref` to link a lowercase name.
- Write types and expressions in backticks: `` `std::vector<int>` ``, `` `size() == 0` ``. It reads as code in every output and avoids `<...>` being taken as HTML.

## A complete example

```cpp
/// @file
/// @brief Fixed-capacity ring buffer used by the audio thread.
#pragma once

#include <cstddef>
#include <optional>

/// @brief Real-time audio utilities.
namespace audio {

/// @brief Single-producer, single-consumer ring buffer with a fixed capacity.
///
/// One thread may call push() and another may call pop() concurrently
/// without locking. Any other concurrent use is a data race.
///
/// @tparam T Element type. Must be nothrow move constructible, because
///           elements are moved on the audio thread where exceptions abort.
template <typename T>
class RingBuffer {
 public:
  /// @brief Creates an empty buffer.
  /// @param capacity Maximum number of elements. Must be a power of two.
  /// @pre `capacity > 0` and `capacity` is a power of two.
  explicit RingBuffer(std::size_t capacity);

  /// @brief Appends an element if there is room.
  /// @param value Element to append; moved from only on success.
  /// @retval true  The element was appended.
  /// @retval false The buffer was full; @p value is unchanged.
  bool push(T&& value) noexcept;

  /// @brief Removes the oldest element.
  /// @return The element, or `std::nullopt` if the buffer is empty.
  std::optional<T> pop() noexcept;

  /// @brief Copies the oldest elements without removing them.
  /// @param[out] out   Destination array with room for @p count elements.
  /// @param      count Number of elements to copy.
  /// @return The number of elements copied, at most @p count.
  /// @note Consumer thread only.
  std::size_t peek(T* out, std::size_t count) const;
};

/// @brief Kinds of underrun handling.
enum class UnderrunPolicy {
  kSilence,     ///< Output zeros until data arrives.
  kRepeatLast,  ///< Repeat the last complete block.
};

}  // namespace audio
```

Note what isn't there: no `@return` on the constructor, no description of how the indices wrap (that's How), no direction on input parameters, and no repeat of "thread-safe" on each member beyond what the class block already says.

## Validation

SKILL.md Steps 2 and 5 run `scripts/check_comments.py`. What it does, so its findings make sense:

- Runs Doxygen on the target files only, with the project's Doxyfile (auto-detected at `Doxyfile`, `docs/Doxyfile` or `doc/Doxyfile`) plus warning options: `WARN_IF_UNDOCUMENTED`, `WARN_IF_DOC_ERROR`, `WARN_IF_INCOMPLETE_DOC`, `WARN_NO_PARAMDOC`, and `EXTRACT_ALL = NO` (which would otherwise silence undocumented-member warnings). Output goes to a temporary directory that is deleted afterwards.
- Generates HTML as well as XML: with XML alone, Doxygen 1.9.8 prints false "parameters ... are not documented" warnings (verified).
- Reads the XML for what Doxygen accepts without a warning: documented entities hidden by a missing `@file` or an undocumented namespace, an empty brief, `///` inside a function body, and `@return` on a function that returns nothing.
- Runs `clang++ -fsyntax-only -Wdocumentation -Wdocumentation-unknown-command` on each file when clang is installed, with include paths and `-std` from `compile_commands.json` if present. GCC has no equivalent. If a file doesn't compile standalone, the summary says so.
- Reports "parameters/return type ... not documented" as `[advisory]`, because a one-line accessor may legitimately have only a `@brief`.
