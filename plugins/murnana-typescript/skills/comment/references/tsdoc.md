# Writing TSDoc Doc Comments

Basis: the TSDoc specification and its standard tag list (Microsoft TSDoc, `tsdoc/src/details/StandardTags.ts`, https://github.com/microsoft/tsdoc, MIT License; see `THIRD_PARTY_NOTICES.md`). Rules are summarized in our own words. Implementation comments (`//`) follow [comment-routing.md](comment-routing.md); link targets follow [declaration-reference.md](declaration-reference.md).

## Contents

1. What a doc comment is for
2. Which declarations get one
3. Layout
4. Tags
5. JSDoc habits to drop
6. Escaping and Markdown
7. Lint codes and fixes

## 1. What a doc comment is for

A `/** ... */` directly above a declaration is the API contract a caller reads in editor hovers and generated docs, without the body or tests in view. Say what the caller may rely on and what the signature cannot express: meaning, units, accepted ranges, defaults, `undefined` handling, side effects, errors. Never describe the implementation ("loops over", "uses a Map"); that is How and belongs in the code.

## 2. Which declarations get one

- Every exported function, class, interface, type alias, enum, namespace and exported `const`/`let`.
- Every non-private member of an exported class or interface: constructor, methods, properties, accessors (document the getter; the setter shares it), call and construct signatures, enum members whose name alone doesn't say what they mean.
- The package entry file: a first comment with `@packageDocumentation` when the project generates docs.
- Skip: `private` / `#private` members, members marked `override` that keep the parent's contract, the implementation signature of an overloaded function, local helpers whose contract is obvious. Document non-exported declarations only when the codebase already does (`--internal`).

## 3. Layout

```ts
/**
 * Summary sentence.
 *
 * @remarks
 * Longer explanation.
 *
 * @typeParam T - ...
 * @param name - ...
 * @returns ...
 * @throws ...
 *
 * @example
 * ```ts
 * ...
 * ```
 *
 * @see {@link Other}
 * @deprecated ...
 */
```

- **Summary**: the text before the first block tag. Keep it to one sentence that stands alone in a hover; don't start with "This function", don't restate the name.
- Put the comment directly above the declaration: above decorators and above `export`. Only whitespace may sit between them; a second `/** */` in between steals the attachment.
- Keep the tag order above. Write each `@param` on one line where possible; continuation lines are fine.

## 4. Tags

Block tags (start a section; one per line):

| Tag | Use |
|---|---|
| `@param name - text` | One per named parameter, in declaration order. **Always the hyphen.** Meaning and accepted range, not the type. For a destructured parameter, pick a readable name (`options`); TypeDoc also accepts `@param options.timeout - ...`. |
| `@typeParam T - text` | One per type parameter: what it stands for and any constraint the caller must meet. |
| `@returns text` | What comes back, including empty / `undefined` / not-found cases. Omit for `void`, `Promise<void>`, `never`, constructors and setters. For `Promise<X>`, describe X ("Resolves to ..."). |
| `@throws text` | One per error a caller should handle, with the condition: `@throws {@link ParseError} if the input is empty`. Only for a visible `throw` or a callee's documented contract. A rejected promise is documented the same way ("Rejects with ..."). |
| `@remarks` | Everything beyond the summary. |
| `@example` | A fenced ```` ```ts ```` block of short, compilable usage. An optional title on the tag line. Several `@example` blocks are allowed. |
| `@defaultValue text` | Default of an optional property or option. Only when the code shows it. |
| `@deprecated text` | What to use instead (and when it will be removed, if known). |
| `@see text` | Related declaration or URL, usually `@see {@link Other} for ...`. |
| `@privateRemarks` | Notes for maintainers that generated docs must not show. A reason for an implementation choice still goes inline, next to the code. |

Modifier tags (no text): `@public`, `@beta`, `@alpha`, `@experimental`, `@internal` (release tags; only if the project uses them, e.g. with API Extractor), `@readonly`, `@sealed`, `@virtual`, `@override`, `@eventProperty`, `@packageDocumentation`. Prefer TypeScript modifiers (`readonly`, `override`, `abstract`) over the tags when the language can say it.

Inline tags (inside text, in braces):

| Tag | Use |
|---|---|
| `{@link Target}` / `{@link Target \| text}` | Link to a declaration (declaration reference syntax) or URL. Link the first mention, not every one. |
| `{@inheritDoc Target}` | Copy the summary, `@remarks`, `@param`, `@typeParam` and `@returns` of another declaration; add only what differs. |
| `{@label NAME}` | Older way to name an overload for links; use only if the codebase does. |

TypeDoc projects may also use TypeDoc's tags (`@category`, `@group`, `@since`, `@hidden`, `{@linkcode}` ...); `lint` allows them when `typedoc` is a dependency. Tags defined in `tsdoc.json` are allowed too.

## 5. JSDoc habits to drop

TypeScript already knows the types and structure. In `.ts` files:

| JSDoc | TSDoc |
|---|---|
| `@param {string} name desc` | `@param name - desc` |
| `@param [name]` (optional) | `@param name - desc` (optionality is in the signature) |
| `@return`, `@returns {T}` | `@returns desc` |
| `@throws {Error}` | `@throws {@link Error} if ...` or plain text |
| `@template T` | `@typeParam T - desc` |
| `@type`, `@typedef`, `@callback`, `@function`, `@class`, `@constructor`, `@extends`, `@implements`, `@memberof`, `@static`, `@async`, `@enum`, `@const` | Nothing: the declaration says it |
| `@private`, `@protected`, `@access` | The TypeScript modifier, or `@internal` |
| `@default` | `@defaultValue` |
| `@author`, `@version`, `@since`, `@todo` | Commit log, `package.json`, a `// TODO(#id): ...` comment (keep `@since` only if the project registers it) |
| `@fileoverview`, `@module`, `@file` | `@packageDocumentation` (TypeDoc projects may keep `@module`) |
| `@link Foo` as a block tag | `{@link Foo}` inside text |

## 6. Escaping and Markdown

- Doc text is Markdown-like: backticks for code, fenced blocks for examples, blank lines between paragraphs.
- A literal `{`, `}` or `@` in text must be escaped (`\{`, `\}`, `\@`) or put in backticks; otherwise TSDoc reads a tag. Email addresses and `@` inside words are fine.
- Don't use HTML for layout (`<br>`, `<p>`); use blank lines.

## 7. Lint codes and fixes

| Code | Fix |
|---|---|
| `PARAM_HYPHEN` | Insert ` - ` after the parameter name. |
| `JSDOC_TYPE`, `JSDOC_OPTIONAL`, `JSDOC_TAG` | Rewrite per section 5. |
| `TAG_UNKNOWN` | Remove it, escape it as `\@word`, or (if the project uses it) register it in `tsdoc.json` / pass `--tags`. |
| `PARAM_UNKNOWN`, `TYPEPARAM_UNKNOWN` | Rename to the real parameter, or delete the tag. In overloads, document a parameter only on the signatures that have it. |
| `PARAM_MISSING`, `TYPEPARAM_MISSING`, `RETURNS_MISSING` | Add the tag from evidence (rule 4), or ask. |
| `PARAM_ORDER` | Reorder to match the signature. |
| `RETURNS_VOID` | Remove `@returns`. |
| `SUMMARY_MISSING`, `SUMMARY_RESTATES` | Write a summary that says what the name can't. |
| `INLINE_UNCLOSED`, `ESCAPE` | Close the inline tag on the same line, or escape / backtick the brace. |
| `LINK_SYNTAX`, `LINK_NAVIGATION`, `LINK_UNRESOLVED` | See [declaration-reference.md](declaration-reference.md). |
| `EXAMPLE_NO_FENCE` | Wrap the example in a ```` ```ts ```` block. |
| `DEPRECATED_EMPTY` | Say what to use instead. |
| `DUPLICATE_TAG` | Merge the repeated sections. |
| `OVERLOAD_DOC` | Move the comment from the implementation to the overload signatures. |
| `ORPHAN_DOC` | See the `ORPHAN_DOC` row in SKILL.md Step 3. |
| `TSDOC(...)` | A message from the `@microsoft/tsdoc` parser; fix the comment as the message says. |
