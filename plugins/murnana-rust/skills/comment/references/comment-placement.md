# Comment Placement: How / What / Why / Why not

Source: Takuto Wada (@t_wada), post on X, 2017-09-05, https://x.com/t_wada/status/904916106153828352 — quoted:

> コードには How テストコードには What コミットログには Why コードコメントには Why not を書こうという話をした

In a reply the same day, the author confirmed that "Why not" means *why another approach was not taken*, and said the point is to leave in code comments the things you *deliberately did not do*, for later readers and your future self. As the questioner put it: what you did can be made clear without comments, but what you deliberately did not do has no way to become visible except a comment.

The rest of this file is this skill's own reading of the principle, applied to Rust, together with points from the wider literature on comments. It is not the author's text.

## The principle

Each kind of artifact is good at carrying one kind of information. Put the information where it is maintained alongside the thing it describes, so it cannot silently go stale.

| Information | Home | Why there |
|---|---|---|
| **How** — the steps the program takes | The code itself | The code is the only exact description of How. A comment that repeats it drifts the first time the code changes. |
| **What** — the behavior the code must have | Tests (unit tests, integration tests, doctests) | A test states expected behavior and fails when it stops being true. |
| **Why** — the reason this change was made | The commit message | The reason belongs to the change at a point in time. `git log` / `git blame` attach it to the exact lines. |
| **Why not** — why the obvious alternative was not used | A code comment | Only a comment stops the next reader at the exact line where they would "fix" it back to the obvious way. |

## Treat it as a mnemonic, not a law

The author introduced the four-way split apologetically as "a bit forced", and in 2019 wrote that when forced to write puzzling code as a workaround, he leaves the Why and Why not in the commit log *or* code comment. Apply it with these adjustments:

- **A Why the line's reader cannot do without stays in the code too.** Developers who need context at a line rarely go searching the commit log, and the commit that explains a line is often not the latest one `git blame` shows (Ousterhout, *A Philosophy of Software Design*, "Comments belong in the code, not the commit log"; Stack Overflow Blog, "Best practices for writing code comments", 2021). Duplicating that Why in the commit message and a comment is fine. Everything else about a change — the ticket, the review discussion, the history — goes only in the commit message.
- **Doc comments are outside the rule.** API documentation states the contract with the caller: what the item does, not how. It is the user-facing *What*, a specification alongside the tests. Do not cut a doc comment down to "Why not only" (see `rustdoc.md`).
- **TODO is its own category.** A TODO reserves future work; a Why not records a decision not to do something. Keep them distinct (see below).

## Decision table for a single comment

Ask in this order; stop at the first match.

1. Does it describe what the next line(s) do? → **How**. Delete. If the code is unreadable without it, rename, extract a function or introduce a named constant/type instead.
2. Does it state a behavior that must hold (input → output, invariant, edge case)? → **What**. Make sure a test asserts it; for public API, state it in the doc comment's contract and back it with a doctest. Then delete the `//` comment.
3. Does it explain why the code was changed, referencing a bug, ticket or request? → **Why**. Move it to the commit message. If someone editing this line would break things without knowing the reason, also keep the reason (not the history) as a comment. Keep only a short pointer (`// See #123`) if the user's team does that.
4. Does it explain why the code is *not* written the obvious way, or warn that a simpler-looking version is wrong? → **Why not**. Keep it; make it meet the conditions below.
5. Is it a `TODO` / `FIXME`? → Keep it only with an issue reference or a concrete condition (see below).
6. Is it a license header, `SAFETY:` justification, or lint suppression reason? → Keep it (see below).

## Comments that are Why not in disguise

These are always kept in Rust, because they explain why the code deviates from the safe or default path:

- `// SAFETY:` on every `unsafe` block — why the preconditions of the unsafe operation hold here. (Clippy's `undocumented_unsafe_blocks` checks for these.)
- The reason next to `#[allow(...)]` / `#[expect(...)]` — why the lint does not apply. Prefer `#[expect(lint, reason = "...")]` when the crate's MSRV allows it.
- Why a `.clone()`, `Box`, `Arc` or allocation is needed where a borrow looks sufficient (borrow-checker constraint).
- Why `unwrap()` / `expect()` cannot fail here — better written as the `expect` message itself.
- Why an ordering, `#[repr(...)]`, or `Ordering::SeqCst` is required instead of a weaker one.
- Why a dependency's obvious API is avoided (known bug, version constraint), with the version or issue.
- Why an optimization was deliberately not done (input is small; measured fast enough).
- Why a refactoring that looks attractive was tried and abandoned — so the next reader does not spend a day repeating it.

## Rust examples

How — delete:

```rust
// Iterate over the items and sum their prices.
let total: u64 = items.iter().map(|i| i.price).sum();
```

What — move to a test:

```rust
// Returns 0 for an empty cart.   <- delete, and add:
#[test]
fn total_of_empty_cart_is_zero() {
    assert_eq!(Cart::new().total(), 0);
}
```

Why — move to the commit message:

```rust
// Changed to u64 because u32 overflowed for wholesale orders (#482).   <- delete
```

Commit message: `:bug: 卸売注文で合計金額が u32 を超えるため u64 に変更 (#482)` (follow the repository's commit conventions).

Why not — keep:

```rust
// Not `sort_unstable`: equal-priority jobs must keep submission order,
// and the scheduler tests rely on it.
jobs.sort_by_key(|j| j.priority);
```

```rust
// SAFETY: `idx` was bounds-checked against `self.len` on the line above,
// and `self.buf` is never shrunk while `self` is borrowed.
unsafe { self.buf.get_unchecked(idx) }
```

```rust
// Not optimized to a single pass: `formulas` holds at most a few dozen
// entries of < 10 chars, so 16 passes are still well under 1 ms.
// Revisit if formulas start being loaded from user files.
for pass in PASSES { ... }
```

```rust
// Kept as a `match` rather than a trait object: the variants need
// `Copy` for the lock-free queue, which `Box<dyn Op>` would break.
// Tried in #311 and reverted.
```

## Writing a good Why not comment

1. **Name the alternative** explicitly ("Not `HashMap`: ...", "Don't replace with `?`: ...").
2. **Give the reason**: the constraint, the measurement, or the spec, and the concrete consequence of the alternative (wrong output, deadlock, regression of #123).
3. **State when the premise stops holding** ("revisit above ~1,000 rows", "remove once tokio#1234 is released"). This lets a later reader delete the comment and the workaround with confidence once the condition is met — write it to be easy to delete.

Keep it next to the line it protects, not in a block at the top of the function.

## TODO / FIXME

- `TODO`: work to do later. `FIXME`: known defect. Use the tags the crate already uses; don't introduce new ones.
- Attach an issue reference or an owner (`// TODO(#123): ...`) and, for "some day" items, a concrete date or event. A TODO is not a commitment; the issue tracker is where the work is tracked.
- Prefer `todo!()` / `unimplemented!()` for unreachable unfinished code paths: they fail loudly instead of silently.
- Don't use TODO to record a decision not to do something; that is a Why not.
