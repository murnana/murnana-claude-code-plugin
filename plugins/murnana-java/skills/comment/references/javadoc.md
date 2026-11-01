# Javadoc Doc Comments

Rules for `/** ... */` doc comments, summarized in our own words from the Java SE 8 `javadoc` tool reference ("javadoc", Java Platform, Standard Edition Tools Reference: https://docs.oracle.com/javase/8/docs/technotes/tools/windows/javadoc.html). Later JDKs keep these rules and add tags; additions are marked **(9+)** or **(18+)**. When this file and the JDK the project uses disagree, the JDK's own documentation wins.

## Contents

1. Where doc comments go
2. Structure of a comment
3. The first sentence
4. HTML, escaping and whitespace
5. Tags and where each may be used
6. Tag syntax and how to write each
7. Referencing program elements
8. Comment inheritance
9. Package and overview comments
10. Doclint
11. Writing style
12. Examples

## 1. Where doc comments go

- `javadoc` reads a doc comment only when it is placed **immediately before** the declaration of a class, interface, enum, annotation type, field, constructor or method. A doc comment anywhere else (inside a method body, before an `import`, before a statement) is ignored.
- Put the doc comment **before the annotations** of the declaration:

  ```java
  /** Returns the cached value, or {@code null} if it expired. */
  @Nullable
  @Override
  public V get(K key) { ... }
  ```

- Only one doc comment per declaration is used: the one closest to the declaration. Don't put an implementation comment `/* ... */` between the doc comment and the declaration.
- A field declaration that declares several variables (`int x, y;`) shares one doc comment; declare documented fields one per line.
- Package comments and the overview comment live in separate files (section 9).

## 2. Structure of a comment

```
/**
 * Main description: first sentence (the summary). Further sentences
 * and paragraphs.
 * <p>
 * More description.
 *
 * @param name   description          <- block tags section
 * @return description
 */
```

- A comment has a **main description** followed by an optional **block tags section**. The main description ends where the first block tag begins. Text after the first block tag can't return to the main description.
- A **block tag** (`@param`, `@return` ...) is recognized only at the **start of a line**, after optional leading whitespace and the leading `*`. An `@` elsewhere is plain text; to start a line with a literal `@`, write `&#64;` or `{@literal @}`.
- An **inline tag** (`{@code ...}`, `{@link ...}` ...) may appear anywhere in the main description or inside a block tag's text.
- A block tag's text runs until the next block tag or the end of the comment.
- Separate paragraphs with `<p>`. The `javadoc` tool does not turn blank lines into paragraphs.

## 3. The first sentence

- The first sentence of the main description is the **summary**: it is copied into the member summary table and the index. It must make sense on its own.
- For English, the first sentence ends at the first period followed by a space, tab or line end, or at the first block tag. (JDK 8 uses this rule unless `-breakiterator` is given; JDK 9+ always uses locale-sensitive `BreakIterator` rules, with the same effect for English.) Abbreviations end it early: in `"Takes a key, e.g. a name."` the summary becomes `"Takes a key, e.g."`. Write `e.g.&nbsp;`, `{@literal e.g. }`, or rephrase ("for example").
- In Japanese text, `。` ends the sentence only when a space, tab or line end follows it, or when `javadoc` runs with `-locale ja_JP`. With the default locale, `値を返す。詳しくは…` makes the whole run the summary (checked with JDK 21). End the first sentence's line right after `。`.
- **(10+)** `{@summary text}` at the start of the main description sets the summary explicitly.
- If an element has no main description of its own and inherits one, the summary is inherited too.

## 4. HTML, escaping and whitespace

- The comment body is **HTML**, not Markdown (**(23+)** `///` Markdown doc comments exist; use them only if the project already does).
- Escape `<`, `>` and `&` as `&lt;`, `&gt;`, `&amp;`, or put the text in `{@code ...}` / `{@literal ...}`, which escape for you. Generic types in prose (`List<String>`) need this.
- Use only valid HTML that the doclint `html` group accepts: no self-closing `<p/>` or `<br/>`, no headings that skip levels or clash with the page's own headings (doclint reports them; prefer bold text or a `<p>` over headings in member comments), close the elements you open, no `<tt>` or other obsolete tags, `<table>` needs a caption or summary for accessibility.
- Leading `*` and the whitespace before it are removed from each line. Lines without a leading `*` keep their leading whitespace.
- Inside `<pre>`, whitespace after the leading `*` is preserved, so indent code samples after the `*`. For a sample containing `@` or `}`/`{`, prefer `<pre>{@code ... }</pre>` (braces must balance) or **(18+)** `{@snippet ...}`.
- Don't put `*/` inside a comment; write `*&#47;`.

## 5. Tags and where each may be used

Columns: **O** overview, **P** package, **T** class/interface/enum/annotation type (type), **F** field, **C** constructor, **M** method.

| Tag | O | P | T | F | C | M | Notes |
|---|---|---|---|---|---|---|---|
| `@author` | ✓ | ✓ | ✓ | | | | Output only with `-author` |
| `@version` | ✓ | ✓ | ✓ | | | | Output only with `-version` |
| `@since` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `@see` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `@deprecated` | | | ✓ | ✓ | ✓ | ✓ | Pair with the `@Deprecated` annotation |
| `@param` | | | ✓ | | ✓ | ✓ | On types: type parameters only (`@param <T>`) |
| `@return` | | | | | | ✓ | Not for `void` or constructors |
| `@throws` / `@exception` | | | | | ✓ | ✓ | Synonyms; prefer `@throws` |
| `@serial` | | ✓ | ✓ | ✓ | | | `include`/`exclude` on package and type |
| `@serialField` | | | | ✓ | | | Only on `serialPersistentFields` |
| `@serialData` | | | | | | ✓ | Only on `writeObject`, `readObject`, `writeExternal`, `readExternal`, `writeReplace`, `readResolve` |
| `{@code}` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `{@literal}` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `{@link}` / `{@linkplain}` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `{@docRoot}` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `{@value}` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Without an argument: only on a constant field |
| `{@inheritDoc}` | | | | | | ✓ | Only in a method's main description, `@param`, `@return`, `@throws` |

Later additions, usable only when the project's JDK supports them: `@hidden` **(9+)**, `{@index}` **(9+)**, `@provides` / `@uses` on modules **(9+)**, `{@summary}` **(10+)**, `{@systemProperty}` **(12+)**, `@spec` **(20+)**, `{@snippet}` **(18+)**, `{@return}` inline form **(16+)**. `@apiNote`, `@implSpec`, `@implNote` are not standard tags; they work only when the build registers them with `-tag apiNote:a:"API Note:"` (and similar), as the JDK itself does.

## 6. Tag syntax and how to write each

**`@param name description`** — One per parameter, in declaration order, every parameter documented. For a type parameter write `@param <T> description`. The description is a phrase (lowercase start, no trailing period needed) saying what the value means and its constraints: `@param timeout the maximum wait, in milliseconds; must be positive`.

**`@return description`** — The value and its meaning in each case, including `null`, empty collections and sentinel values. Omit for `void` and constructors. **(16+)** `{@return description}` at the start of the main description writes both the first sentence and `@return`.

**`@throws ClassName description`** — Name the class (simple name if imported). Write the condition, starting with "if": `@throws IllegalArgumentException if {@code timeout} is negative`. Document every checked exception in the `throws` clause and the unchecked exceptions callers are expected to handle or avoid. Don't add unchecked exceptions to the `throws` clause just to document them.

**`@deprecated description`** — First sentence says since when and what to use instead, with a link: `@deprecated since 2.3, use {@link #open(Path)} instead`. Always add the `@Deprecated` annotation too (**(9+)** with `since`/`forRemoval` as appropriate).

**`@since version`** — The product version in which the element was added (`@since 1.4`). On a member, only when it is newer than its enclosing type.

**`@see reference`** — Three forms: `@see "A book or text"`, `@see <a href="URL">label</a>`, `@see package.Class#member label`. One reference per tag. Use for related elements the reader should also look at, not for things already linked in the text.

**`@author name`, `@version text`** — Use only if the project already does; VCS history usually serves this better.

**`{@code text}`** — Code font, HTML-escaped, no tag interpretation inside. Use for keywords, names, literals and expressions: `{@code null}`, `{@code true}`, `{@code List<String>}`. Braces inside must balance.

**`{@literal text}`** — Like `{@code}` without the code font.

**`{@link reference label}`** — A link in code font. Link the first mention of another API element in a comment, not every mention. **`{@linkplain reference label}`** — same, in plain text font, for links read as prose.

**`{@value reference}`** — The value of a constant: `{@value #MAX_SIZE}` or, inside the constant's own comment, `{@value}`.

**`{@docRoot}`** — The relative path to the generated doc root, for links to files under `doc-files/`: `<a href="{@docRoot}/doc-files/format.html">`.

**`{@inheritDoc}`** — Copies the inherited text at this point (section 8).

**`@serial`, `@serialField`, `@serialData`** — For `Serializable` classes whose serialized form is part of the public contract. `@serial field-description` on each serializable field; `@serial include|exclude` on a type or package to control whether it appears on the Serialized Form page.

**Recommended block tag order:** `@param` (type parameters first, then parameters in declaration order), `@return`, `@throws` (alphabetically or by importance, consistently), `@author`, `@version`, `@see`, `@since`, `@serial` / `@serialField` / `@serialData`, `@deprecated`.

## 7. Referencing program elements

Used by `@see`, `{@link}`, `{@linkplain}`, `{@value}`:

| Form | Example |
|---|---|
| Member of the current class | `#size()`, `#MAX_SIZE` |
| Type (imported or in scope) | `Formatter`, `Map.Entry` |
| Member of another type | `Formatter#format(String, Object...)` |
| Fully qualified | `java.util.List#add(Object)` |
| Package | `java.util.concurrent` |
| Constructor | `#Cache(int)`, `Cache#Cache(int)` |

- Separate the member with `#`. Give parameter types (simple names if imported, no parameter names needed) to pick an overload; without them the first matching name is used. Varargs: `String...`. Generic parameters use the erasure: `#put(Object, Object)`.
- After the reference, the rest of the tag text is the label: `{@link #close() closing the stream}`.
- A reference that can't be resolved is a doclint `reference` error. Don't link to elements the generated docs won't include (private members in public docs).

## 8. Comment inheritance

When a method overrides a superclass method or implements an interface method, `javadoc` fills in what the method's own comment leaves out:

- **Inherited automatically** if missing: the main description, each `@param`, `@return`, and each `@throws` **for an exception declared in this method's `throws` clause**.
- **Not inherited**: other tags (`@see`, `@since`, `@deprecated` ...), and comments of constructors, fields and types.
- **`{@inheritDoc}`** inserts the inherited text explicitly, so the comment can add to it: `{@inheritDoc} <p>This implementation caches the result.`. Valid in the main description, `@param`, `@return`, `@throws` of methods.
- Source search order: interfaces the class directly implements (in declaration order), then the superclass chain, repeating the search recursively, up to the first comment that has the needed part. Text is inherited only from supertypes whose source `javadoc` can read (on `-sourcepath`, or the JDK's own sources for JDK types); otherwise the override shows no description.
- Write an override comment only to state what changes (stronger guarantees, different performance, side effects). If nothing changes, leave the override without a doc comment rather than copying text. Projects often still require a comment on every public method; then use `{@inheritDoc}` plus the difference.

## 9. Package and overview comments

- **Package comment**: `package-info.java` in the package directory, containing the doc comment followed by the `package` declaration (and package annotations). The older alternative `package.html` holds the comment as HTML body content, without `/** */`. Use one or the other, not both; prefer `package-info.java`.

  ```java
  /**
   * Provides rate limiters for outbound HTTP clients.
   *
   * @since 2.0
   */
  package com.example.http.ratelimit;
  ```

- The package comment's first sentence is the summary on the overview page. Describe what the package provides and point to its main entry types.
- **Overview comment**: an HTML file passed with `-overview <file>` (conventionally `overview.html` in the source root). Its `<body>` content is the comment; tags allowed: `@see`, `@since`, `@author`, `@version` and inline tags.
- **(9+)** Modules: the doc comment goes before the `module` declaration in `module-info.java`.
- Files referenced from comments (images, sample files) go in a `doc-files` directory next to the source; `javadoc` copies it unchanged.

## 10. Doclint

`javadoc` (since 8) and `javac` check comments with doclint.

- Options: `-Xdoclint` (default checks), `-Xdoclint:none`, `-Xdoclint:all`, and groups with an optional access level, combined with commas: `-Xdoclint:all,-missing`, `-Xdoclint:all/protected`.
- Groups: `accessibility` (for example tables without captions), `html` (invalid or misplaced HTML, self-closing tags, unknown entities), `missing` (missing comments or tags such as `@param` / `@return`), `reference` (unresolvable `{@link}` / `@see`, `@param` names that don't exist, `@throws` for something that isn't a `Throwable`), `syntax` (unescaped `<`/`&`, malformed tags).
- In JDK 8 and later, doclint errors fail the `javadoc` run by default, which commonly breaks Maven release builds. Fix the comment rather than disabling doclint, unless the project already disables it.
- In this skill, `java_comments.py lint` runs `javac -Xdoclint:all/protected` (or `/package`) on the target files only, keeps only diagnostics that appear with doclint and not without it (so missing dependencies don't count as comment errors), and drops `unknown tag` for tags given with `--tags`. Add `--classpath` so references to dependency types resolve.

## 11. Writing style

These are common conventions, not rules of the `javadoc` tool; follow the project's style where it differs.

- Write the contract, independent of the implementation: what callers may rely on, preconditions, postconditions, side effects, thread safety, `null` handling, units and ranges. Leave out how it works unless callers depend on it (for example algorithmic complexity they may rely on).
- English: start method summaries with a third-person verb ("Returns the ...", "Creates a ..."), not "This method ...". Class summaries are noun phrases or "Represents ...". Japanese: 「〜を返す。」「〜を表す。」 in plain form (である調), one style throughout.
- Don't restate the name: `/** Gets the name. */ getName()` adds nothing. Say what the name can't: format, when it's `null`, whether it's a copy.
- Use `{@code}` for code words, `{@link}` for the first mention of another element.
- Keep doc comments in sync with signatures: renaming a parameter means renaming its `@param`.
- Don't document private elements with `/** */` unless the project generates private docs or uses them for IDE hints; a short implementation comment is enough there.

## 12. Examples

Method:

```java
/**
 * Returns the value mapped to {@code key}, loading it with the
 * configured loader if it is absent or expired.
 * <p>
 * Concurrent calls for the same key load it only once; the other
 * callers block until that load completes.
 *
 * @param key the key to look up; must not be {@code null}
 * @return the current value, never {@code null}
 * @throws NullPointerException if {@code key} is {@code null}
 * @throws CacheLoadException if the loader fails; the key stays absent
 * @see #getIfPresent(Object)
 * @since 1.2
 */
public V get(K key) throws CacheLoadException { ... }
```

Generic type:

```java
/**
 * A fixed-capacity cache that evicts the least recently used entry.
 * Instances are safe for use by multiple threads.
 *
 * @param <K> the type of keys
 * @param <V> the type of cached values
 */
public final class LruCache<K, V> { ... }
```

Override that only adds:

```java
/**
 * {@inheritDoc}
 * <p>
 * This implementation never blocks; it returns an empty optional
 * while a load is in progress.
 */
@Override
public Optional<V> peek(K key) { ... }
```

Deprecation:

```java
/**
 * Opens the file at {@code name}.
 *
 * @param name the file name
 * @return the opened stream
 * @throws IOException if the file can't be opened
 * @deprecated since 3.0, use {@link #open(Path)}, which reports the
 *             failing path in the exception
 */
@Deprecated
public InputStream open(String name) throws IOException { ... }
```
