# XML Documentation Comments (`///`)

Based on Microsoft Learn, "Generate XML API documentation comments" (https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/) and "Recommended XML tags for C# documentation comments" (https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags), © Microsoft Corporation, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Summarized, reorganized and adapted by AI (Claude); not the original text and not endorsed by Microsoft.

## What a doc comment is for

- A `///` comment documents the API for its callers. The compiler merges it with the signatures into an XML file when `GenerateDocumentationFile` (or `DocumentationFile`) is set; IntelliSense, DocFX, Sandcastle and Doxygen read it.
- State the contract: what the member does, what each input means, what comes back, what can be thrown, and which conditions callers must meet. Do not describe the implementation (How); put implementation-only notes in `//` comments.
- Doc comments are not metadata: they are not in the compiled assembly and not reachable by reflection.

## Baseline rules

- Document every publicly visible type and member, for consistency. With the documentation file enabled, the compiler warns `CS1591` for each one without a comment.
- Documenting private members is possible but exposes internals; do it only when the project or user wants it.
- Every documented type and member gets at least `<summary>`.
- Write complete sentences ending with a period (in Japanese, end with 「。」).
- The XML must be well formed, or the compiler warns and the output file records an error.
- Namespaces cannot carry doc comments.
- For partial types, comments from all parts are merged. If both declarations of a partial member have comments, the implementing declaration wins.
- `///` lines without any tags are copied as plain text but most tools, including IntelliSense, ignore them. Always use tags.

## Delimiters

- Use `///` (the form templates and docs use). White space right after `///` is not included in the output.
- `/** ... */` also works, but leading `*` patterns are stripped only when every line uses the same pattern; mixed spaces and tabs break it. Do not introduce `/** */` unless the file already uses it.

## Escaping and generics

- Write `<` and `>` in text as `&lt;` and `&gt;` (also `&amp;` for `&`).
- In `cref`, refer to generics with braces: `cref="List{T}"`, `cref="IDictionary{TKey, TValue}"`. The compiler reads the braces as angle brackets.

## Tags

The compiler checks tags marked ✓ (warnings on mismatch). IntelliSense shows the ones marked 💡.

### General

| Tag | Use |
|---|---|
| `<summary>` 💡 | One or two sentences describing the type or member. Required. |
| `<remarks>` | Supplementary detail: usage notes, thread safety, performance, design limits. May be long. Some tools (DocFX) render Markdown inside a `CDATA` section. |

### Members

| Tag | Use |
|---|---|
| `<param name="x">` ✓ 💡 | One per parameter. `name` must match the signature exactly; missing or wrong names cause warnings. |
| `<paramref name="x"/>` | Mark a parameter name inside other text. |
| `<returns>` 💡 | The return value of a non-void method. For `Task<T>`, describe the `T` result ("A task whose result is ..."). Omit for `void` and plain `Task`. |
| `<value>` 💡 | What a property's value represents (units, range, default). |
| `<exception cref="T">` ✓ | Each exception a caller should expect, with the condition: "<paramref name="path"/> is <see langword="null"/>." Usable on methods, properties, events and indexers. |
| `<typeparam name="T">` ✓ 💡 | One per type parameter of a generic type or method. |
| `<typeparamref name="T"/>` | Mark a type parameter name inside other text. |

### Links and references

| Tag / attribute | Use |
|---|---|
| `<see cref="M"/>` ✓ | Inline link to a code element. Give link text with `<see cref="M">text</see>`. The compiler checks the target exists and honors `using` directives. |
| `<see href="https://...">text</see>` | Inline clickable URL. Use `href`, not `cref`, for web pages; `cref` with a URL produces no link. |
| `<see langword="null"/>` | Language keyword (`null`, `true`, `false`, `default`, ...). |
| `<seealso cref="M"/>` ✓, `<seealso href="...">` | Entry in a "See also" section. Cannot be nested inside `<summary>`. |

### Formatting

| Tag | Use |
|---|---|
| `<para>` | Paragraph inside `<summary>`, `<remarks>`, `<returns>` (double spacing). |
| `<br/>` | Single line break. |
| `<list type="bullet\|number\|table">` | Lists with `<item><description>` (and `<term>`, `<listheader>` for tables and definition lists). |
| `<c>` | Inline code. Prefer it over the deprecated `<tt>`. |
| `<code>` | Multi-line code, usually inside `<example>`. |
| `<example>` | Usage example of the member. |
| `<b>`, `<i>`, `<u>`, `<a href>` | Basic HTML formatting the compiler and Visual Studio accept. Use sparingly. |

### Reuse

| Tag | Use |
|---|---|
| `<inheritdoc/>` | Inherit docs from the base class, interface or overridden member. Use it on overrides and implementations instead of copying text. `cref` picks a specific source (for example, the sync overload for its async version); `path` filters tags with XPath. Own tags on the member are not overridden. Visual Studio shows inherited docs even without the tag, but the generated XML file does not contain them, so add `<inheritdoc/>` explicitly in distributed libraries. |
| `<include file='f.xml' path='doc/members/member[@name="id"]/*'/>` ✓ | Pull docs from an external XML file. Use only when the project already does. |

### Others

- `<safety>`: states the conditions callers must guarantee for a requires-unsafe member under the updated memory safety model (preview in C# 15 / .NET 11). The compiler does not process it. Add it only for projects that opt into that model.
- Custom tags are copied verbatim to the output; use them only when the project's documentation tool supports them (for example, Sandcastle's `<note>`).

## Writing the text

- `<summary>` of a method starts with a verb describing the effect ("Gets...", "Parses...", or 「〜を取得します。」). For a class, describe what it represents or is responsible for. For a Boolean property, use "Gets a value indicating whether ...".
- Do not repeat the member name or type ("Gets the name." for `Name` adds nothing; say what the name identifies, its format or when it can be empty).
- State nullability, units, ranges and side effects callers depend on.
- Put the contract in the doc comment, the reasoning about implementation choices in `//` comments.

## Example

```csharp
/// <summary>
/// Reads the save file at the given path and restores the player state.
/// </summary>
/// <param name="path">Absolute path of the save file.</param>
/// <param name="cancellationToken">Token to cancel the read.</param>
/// <returns>
/// A task whose result is the restored state, or <see langword="null"/> if the file is empty.
/// </returns>
/// <exception cref="ArgumentNullException"><paramref name="path"/> is <see langword="null"/>.</exception>
/// <exception cref="FileNotFoundException">No file exists at <paramref name="path"/>.</exception>
/// <seealso cref="SaveAsync(PlayerState, string, CancellationToken)"/>
public Task<PlayerState?> LoadAsync(string path, CancellationToken cancellationToken = default)
```

```csharp
/// <inheritdoc/>
/// <remarks>This implementation caches results for 5 minutes.</remarks>
public override Task<User?> FindAsync(int id) { ... }
```

## Compiler warnings to watch

| Warning | Meaning |
|---|---|
| `CS1570` | Badly formed XML |
| `CS1571` / `CS1572` / `CS1573` | Duplicate `<param>`, `<param>` for a parameter that does not exist, parameter without `<param>` while others have one |
| `CS1574` / `CS1584` | `cref` cannot be resolved / has bad syntax |
| `CS1587` | `///` placed where no element follows (use `//` there) |
| `CS1591` | Missing doc comment on a publicly visible type or member |
| `CS1711` / `CS1712` | `<typeparam>` for a nonexistent / missing type parameter |
