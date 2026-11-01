# rustdoc Doc Comments

Based on *Rust by Example*, "Documentation" (https://doc.rust-lang.org/rust-by-example/meta/doc.html, source `src/meta/doc.md` in https://github.com/rust-lang/rust-by-example), Copyright (c) 2014 Jorge Aparicio, licensed under MIT or Apache-2.0. Adapted and extended for this skill; see the plugin's `THIRD_PARTY_NOTICES.md` for the license text. Items marked *(added)* are not from that chapter.

## Commands

| Command | Effect |
|---|---|
| `cargo doc` | Build documentation into `target/doc`. |
| `cargo doc --open` | Build and open it in the browser. |
| `cargo doc --no-deps` *(added)* | Build only this crate's docs; faster for checking warnings. |
| `cargo test` | Run all tests, including documentation tests. |
| `cargo test --doc` | Run only documentation tests. |

These commands invoke `rustdoc` (and `rustc`) as needed. Outside Cargo, a doctest is run by building the code as a library and pointing `rustdoc` at it:

```shell
$ rustc doc.rs --crate-type lib
$ rustdoc --test --extern doc="libdoc.rlib" doc.rs
```

## Doc comments

- `///` documents the item that follows. These are the comments `rustdoc` compiles into documentation, and they support Markdown.
- `//!` documents the enclosing item — put it at the top of `lib.rs` for the crate, or at the top of a module file. *(added)*
- Fenced code blocks inside doc comments are doctests: `rustdoc --test` / `cargo test --doc` compiles and runs them.
- Link to other items with intra-doc links, e.g. `[name](Person::name)` or `` [`Person`] ``.

Example (adapted from the chapter):

````rust
/// A human being is represented here.
pub struct Person {
    /// A person must have a name, no matter how much Juliet may hate it.
    name: String,
}

impl Person {
    /// Creates a person with the given name.
    ///
    /// # Examples
    ///
    /// ```
    /// use doc::Person;
    /// let person = Person::new("name");
    /// ```
    pub fn new(name: &str) -> Person {
        Person { name: name.to_string() }
    }

    /// Gives a friendly hello!
    ///
    /// Says "Hello, [name](Person::name)" to the `Person` it is called on.
    pub fn hello(&self) {
        println!("Hello, {}!", self.name);
    }
}
````

Caution *(added)*: `name` is a private field, so `[name](Person::name)` triggers `rustdoc::private_intra_doc_links` in `cargo doc` (the link only resolves with `--document-private-items`). In public docs, link only to public items, or describe the private detail in words.

## Doc attributes

The most common `#[doc]` attributes:

| Attribute | Use | Example |
|---|---|---|
| `#[doc(inline)]` | Show a re-exported item's docs in place, instead of linking out to a separate page. | `#[doc(inline)] pub use bar::Bar;` |
| `#[doc(no_inline)]` | Keep a re-export as a link instead of inlining it. | `#[doc(no_inline)] pub use crate::mem::drop;` (libcore prelude) |
| `#[doc(hidden)]` | Leave the item out of the documentation. | `#[doc(hidden)] pub use self::async_await::*;` (futures-rs) |

Use `#[doc(hidden)]` for items that must be `pub` for macros or sibling crates but are not part of the supported API; say so in a `//` comment (it is a Why not).

## Conventions for the summary and sections

Summarized from RFC 1574, "More API Documentation Conventions" (https://rust-lang.github.io/rfcs/1574-more-api-documentation-conventions.html, linked from the chapter's "See also"; rust-lang/rfcs, MIT or Apache-2.0). Items marked *(added)* are not from the RFC.

- The first line is a single-line, short summary sentence in third person singular present indicative ("Returns ...", not "Return ..."). rustdoc uses it as the summary throughout its output.
- Leave a blank `///` line between the summary and the rest. *(added)*
- Common headings, in this order: `# Examples`, `# Panics`, `# Errors`, `# Safety`, `# Aborts`, `# Undefined Behavior`. Use only the ones that apply.
  - `# Panics`: the circumstances in which the function panics.
  - `# Errors`: which errors are returned and when. *(added: wording)*
  - `# Safety`: for `unsafe fn` / `unsafe trait`, the invariants the caller is expected to uphold.
- Everything public should have examples. Code fences in doc comments default to Rust; no `rust` tag is needed.
- Module-level docs give a high-level summary of the module's contents; a little duplication with type-level docs is fine.
- Prefer line comments (`//`, `///`) over block comments.
- Write examples as a user would: `use` the crate by its name; prefer `?` over `unwrap()` (wrap with hidden `# fn main() -> Result<(), Box<dyn std::error::Error>> {` ... `# Ok(()) }`). Lines starting with `# ` are compiled but hidden from the rendered docs. *(added)*
- Doctest fence attributes: `no_run` (compiled, not run — e.g. network access), `should_panic`, `compile_fail`, `ignore` (avoid; not even compiled). Each needs a reason. *(added)*

## Lints that enforce documentation *(added)*

| Lint | Checks |
|---|---|
| `missing_docs` (rustc, allow by default) | Every public item has a doc comment. Enable with `#![warn(missing_docs)]`. |
| `rustdoc::broken_intra_doc_links` (warn) | Intra-doc links resolve. |
| `rustdoc::private_intra_doc_links` (warn) | Public docs don't link to private items. |
| `clippy::missing_errors_doc` (pedantic) | `pub fn` returning `Result` has `# Errors`. |
| `clippy::missing_panics_doc` (pedantic) | `pub fn` that may panic has `# Panics`. |
| `clippy::missing_safety_doc` (style) | `pub unsafe fn` has `# Safety`. |
| `clippy::undocumented_unsafe_blocks` (restriction) | `unsafe` blocks have a `// SAFETY:` comment. |

## Further reading (linked, not bundled)

- The Rust Book, "Making Useful Documentation Comments": https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html#making-useful-documentation-comments
- The rustdoc Book: https://doc.rust-lang.org/rustdoc/index.html
- The Reference, "Doc comments": https://doc.rust-lang.org/stable/reference/comments.html#doc-comments
- RFC 1946, intra-rustdoc links: https://rust-lang.github.io/rfcs/1946-intra-rustdoc-links.html
