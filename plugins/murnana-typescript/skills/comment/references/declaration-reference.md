# TSDoc Declaration References

Source: Microsoft TSDoc, `tsdoc/src/beta/DeclarationReference.grammarkdown` (https://github.com/microsoft/tsdoc/blob/main/tsdoc/src/beta/DeclarationReference.grammarkdown), Copyright (c) Microsoft Corporation, MIT License. Summarized and adapted; the full license is in the plugin's `THIRD_PARTY_NOTICES.md`.

A declaration reference names a TypeScript declaration. Use it as the target of `{@link ...}`, `{@inheritDoc ...}` and `@see {@link ...}`. The grammar is in TSDoc's `beta` folder: tools differ in support. Before writing references, check the project's doc tool:

- **TypeDoc** resolves declaration references in `{@link}` (it also has a TypeScript-resolution mode, `useTsLinkResolution`, that resolves names as the TypeScript language service does).
- **API Extractor / `@microsoft/tsdoc` parser** use the older TSDoc reference syntax by default (`{@link my-package#Foo.bar}`, overloads selected with `{@label}`). If the project uses it, follow the syntax already in the codebase instead of the beta grammar below.
- No doc tool, or TypeDoc: use the declaration reference syntax below. Prefer the simplest form: a plain name in scope (`{@link Foo}`); for members, `Foo#bar` (instance) and `Foo.bar` (static). Editor hovers resolve plain names and `Foo.bar` best; that is fine, the generated docs are the target.

## Overall shape

```
[module-source "!"] [component-path] [":" meaning]
```

| Form | Meaning | Example |
|---|---|---|
| `SymbolReference` | Symbol resolved from the current scope (shorthand) | `{@link Parser}` |
| `ModuleSource!` | The module itself | `{@link my-lib!}` |
| `ModuleSource!SymbolReference` | An export of a module | `{@link my-lib!Parser}` |
| `ModuleSource!~SymbolReference` | A local (non-exported) declaration of a module | `{@link my-lib!~helper}` |
| `!SymbolReference` | A global symbol | `{@link !Promise}` |
| (empty) | An empty reference | — |

Module source is a package name or path (`my-lib`, `my-lib/sub`, `./util`). Quote it with `"..."` if it contains `!`.

## Navigation between components

| Punctuator | Navigates via | Use for | Example |
|---|---|---|---|
| `.` | `exports` | Namespace members, static class members, enum members | `Shapes.Circle`, `Parser.create`, `Color.Red` |
| `#` | `members` | Instance members of a class or interface | `Parser#parse`, `Options#timeout` |
| `~` | `locals` | Declarations local to a symbol or module (not exported) | `my-lib!~cache` |

A component is one of:

- A plain identifier: any characters except `"`, whitespace, line terminators and the punctuators `{ } ( ) [ ] ! . # ~ : , @`.
- A quoted string, for names with those characters: `Config#"a.b"`, `Map#"key with space"`. Escapes follow JavaScript string escapes (`\"`, `\\`, `\n`, `\x41`, `\u0041`, `\u{1F600}`).
- A bracketed declaration reference, for computed / symbol-keyed members: `Collection#[!Symbol.iterator]`.

## Meanings (disambiguation)

Append `:keyword` when one name has several meanings (for example a class and a namespace merged under the same name, or a type and a value).

| Keyword | Selects |
|---|---|
| `class` | Class |
| `interface` | Interface |
| `type` | Type alias |
| `enum` | Enum |
| `namespace` | Namespace / module |
| `function` | Function |
| `var` | Variable |
| `constructor` | Constructor |
| `member` | Class member or enum member |
| `event` | Event |
| `call` | Call signature |
| `new` | Construct signature |
| `index` | Index signature |
| `complex` | Any complex type |

Overloads: add an index.

| Form | Example |
|---|---|
| `:keyword(n)` | `parse:function(1)` |
| `:(n)` | `parse:(1)` |
| `:n` | `parse:1` |

Check how the project's doc tool numbers overloads before using an index; add the meaning only when the name is actually ambiguous.

## Examples

```ts
/**
 * Formats a value for display.
 *
 * @see {@link Parser#parse} for the reverse operation.
 * @see {@link my-lib!Options#locale} for locale handling.
 * @see {@link Shapes.Circle:class} (the class, not the namespace of the same name).
 * @see {@link Collection#[!Symbol.iterator]} for iteration order.
 * @see {@link !Intl.NumberFormat} for the underlying formatter.
 */
```

Link text: `{@link Parser#parse | parse()}` shows `parse()` as the label. A URL also works: `{@link https://example.com | the spec}`.

## Pitfalls

- `Foo.bar` means a static / exported `bar`; an instance method needs `Foo#bar`.
- Names containing a punctuator (`. # ~ : ! , ( ) [ ] { } @`), `"` or whitespace must be quoted. `-` and `$` need no quotes.
- The grammar notes an unresolved ambiguity between a symbol path and a module source; always end a module source with `!` so the parser can tell them apart.
- Reference only declarations that exist. Verify with Grep before writing the link.

## Lint codes

| Code | Meaning and fix |
|---|---|
| `LINK_SYNTAX` | The reference breaks the grammar (unquoted punctuation or space, unknown `:meaning`, empty component, unbalanced quotes/brackets). Fix per the tables above. |
| `LINK_NAVIGATION` | `.` used for an instance member (use `#`), `#` used for a static member (use `.`), or `#` on an enum/namespace member (use `.`). Checked for classes declared in the same file. Ignore it in API Extractor projects that use the older `Foo.bar` style throughout. |
| `LINK_UNRESOLVED` | The first component is not declared or imported in this file and is not a common global, or a same-file class has no such member. Confirm the target exists (LSP `workspaceSymbol` or Grep). If it exists elsewhere, keep the link and say so in the report, or add a module source (`pkg!Name`). If it doesn't exist, fix or remove the link. |
