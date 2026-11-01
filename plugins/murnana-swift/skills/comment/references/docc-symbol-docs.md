# DocC Documentation Comments

Syntax and content rules for Swift documentation comments that DocC compiles into reference documentation.

## Comment syntax

- Start each line with `///`. Turning an existing `//` comment on a declaration into a documentation comment only needs the extra `/`.
- `/** … */` also works; everything between the delimiters becomes documentation. Follow whichever form the project already uses.
- Content is DocC documentation markup (Markdown plus DocC extensions). See "Formatting" below.

## Summary (first line)

- The first line (first paragraph) is the summary: one sentence or sentence fragment, ideally 150 characters or fewer.
- Plain text only: no links, no technical jargon, no other symbol names.
- It adds to the symbol's name rather than repeating it.

```swift
/// Eat the provided specialty sloth food.
mutating public func eat(_ food: Food, quantity: Int) throws -> Int {
```

## Discussion

Paragraphs after the summary, separated by a blank `///` line, form the Discussion section. Write them only when there is more to say. What to cover depends on the symbol:

| Symbol | Cover |
|---|---|
| Property | How it affects the behavior of its owner; typical usage; permitted and default values |
| Method | Usage patterns, side effects, other behaviors; whether it runs asynchronously or is expensive |
| Enumeration case, constant | What it represents, briefly |

Things a signature cannot show and a discussion should: boundary conditions, side effects, errors, relationships and dependencies between components.

## Parameters

Document each parameter on its own: its purpose and, where needed, the range of acceptable values. Place them after the summary (or after the Discussion).

Two equivalent forms; use one consistently.

Parameters section (plural keyword, nested items indented two spaces):

```swift
/// - Parameters:
///   - food: The food for the sloth to eat.
///   - quantity: The quantity of the food for the sloth to eat.
```

Parameter fields (singular keyword, one top-level item per parameter):

```swift
/// - Parameter food: The food for the sloth to eat.
/// - Parameter quantity: The quantity of the food for the sloth to eat.
```

- The list marker can be `-`, `*` or `+`; keywords are case-insensitive. Use `-` and the capitalized keyword unless the project differs.
- Use the **internal** parameter name, not the argument label. For `firstIndex(of element:)`, document `element`, not `of`. Labels like `of`, `in`, `with`, `at`, `to`, `by` make call sites read well but say nothing on their own.
- Add more detail where the name doesn't make it obvious: the effect of `true` vs `false` for a `Bool`, the effect of each case for an enumeration parameter, the inputs and output of a closure parameter.

Multi-paragraph descriptions: indent continuation paragraphs so they line up with the start of the item's text. In a Parameters section that is four spaces after `///` (aligned with the parameter name); in a Parameter field it is two spaces (aligned with the `P` of `Parameter`). Putting the first paragraph on its own indented line can make this clearer:

```swift
/// - Parameters:
///   - mode:
///     The scheduling mode to use.
///
///     Pass `.immediate` to run before returning, or `.deferred` to enqueue.
```

## Returns

- One `- Returns:` item, after the summary, for every method that returns a value.
- For an optional return value, say when it is `nil`.
- Continuation paragraphs are indented two spaces (aligned with the `R`).
- Only one Returns item; more than one is undefined behavior.

```swift
/// - Returns: The sloth's energy level after eating.
```

## Throws

- One `- Throws:` item, after the summary, for every method that can throw.
- Explain the circumstances that cause each error and name the error types or cases.
- Continuation paragraphs are indented two spaces (aligned with the `T`).
- Only one Throws item; more than one is undefined behavior.

```swift
/// - Throws: `SlothError.tooMuchFood` if the quantity is more than 100.
```

## Full example

```swift
/// Eat the provided specialty sloth food.
///
/// Sloths love to eat while they move very slowly through their rainforest
/// habitats. They're especially happy to consume leaves and twigs, which they
/// digest over long periods of time, mostly while they sleep.
///
/// When they eat food, a sloth's `energyLevel` increases by the food's `energy`.
///
/// - Parameters:
///   - food: The food for the sloth to eat.
///   - quantity: The quantity of the food for the sloth to eat.
///
/// - Returns: The sloth's energy level after eating.
///
/// - Throws: `SlothError.tooMuchFood` if the quantity is more than 100.
mutating public func eat(_ food: Food, quantity: Int) throws -> Int {
```

## Formatting

Use DocC documentation markup inside documentation comments.

| Need | Syntax | Use for |
|---|---|---|
| Bold | `**text**` or `__text__` | Labels, names that need emphasis |
| Italic | `*text*` or `_text_` | Introducing a new or alternative term |
| Code voice | `` `text` `` | Short inline code: values, types, signatures |
| Symbol link | ` ``Symbol`` `, ` ``Type/member`` ` | Another documented symbol in the project; prefer it over code voice so readers can navigate |
| Code listing | Fenced block opened with three backticks and the lowercase language name (`swift`, `bash`, `json`, …) | Multi-line examples |
| Bulleted list | `-`, `*` or `+` and a space | Items in any order (two or more items) |
| Numbered list | `1.` and a space | Steps in order (two or more items) |
| Term list | `- term Name: definition` | Term–definition pairs |
| Section header | `### Title` | Occasionally, to structure a long symbol discussion |

- Symbol link paths may start with the module name or a top-level symbol (` ``SlothCreator/CareSchedule/Event`` ` or ` ``CareSchedule/Event`` `).
- Indent code listings with spaces, not tabs, or DocC loses the indentation.
- Don't put images or code listings between list items.
- Don't confuse the `- Parameters:` / `- Returns:` / `- Throws:` items with ordinary bulleted lists: they are recognized only by their keywords.
- When an in-source comment grows too large (long examples, images), suggest a documentation extension file in the `.docc` catalog instead of making the comment longer.

---

Source: summarized and adapted from "Writing Symbol Documentation in Your Source Files" (https://www.swift.org/documentation/docc/writing-symbol-documentation-in-your-source-files) and "Formatting Your Documentation Content" (https://www.swift.org/documentation/docc/formatting-your-documentation-content), Swift-DocC documentation, Copyright (c) 2021-2026 Apple Inc. and the Swift project authors, licensed under the Apache License 2.0. Modified: condensed, reorganized and rewritten as instructions for writing comments; the `mode` parameter example is new. See `THIRD_PARTY_NOTICES.md` at the plugin root.
