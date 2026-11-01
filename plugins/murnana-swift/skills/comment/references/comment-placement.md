# Where Each Piece of Information Goes

Based on Takuto Wada (@t_wada)'s principle, posted on 2017-09-05 (https://x.com/t_wada/status/904916106153828352): code holds How, test code holds What, the commit log holds Why, and code comments hold Why not. Asked whether "Why not" meant "why another approach was not adopted", he confirmed it, adding that the things you deliberately *don't* do are what to leave in comments, for later readers and for yourself. The principle is a mnemonic, not a strict rule; he himself later wrote that a workaround's Why and Why not go into "the commit log or code comments".

## Why each place

| Information | Place | Reason |
|---|---|---|
| How | Code | Code is what runs, so it is the only description that cannot drift. Wanting to explain How in a comment is a signal to rename or restructure. |
| What | Tests | A passing test is an executable specification that cannot go stale. Test names should read as statements of the specification. |
| Why (this change) | Commit message | It is kept next to the diff it explains and can be found line by line with `git blame`. |
| Why not | Code comment | Code can only show what was done. A choice *not* taken is invisible in code, so a comment that stays next to the code is the only place it can live. |

## Supplement: essential Why also goes in the code

John Ousterhout (*A Philosophy of Software Design*) argues that comments belong in the code, not the commit log: a developer who needs the information is unlikely to search the log, and the commit that holds it may not be the latest one touching the line. So:

- Put the Why of a *change* in the commit message.
- Also put in a comment any Why that a reader of the *current code* cannot do without, even if it duplicates the commit message.
- Less experienced writers find Why not hard to anticipate; writing the Why first is a valid way to get there.

## Documentation comments are separate

The principle targets implementation comments. A documentation comment (`///`) on a public API is a specification for callers, the same role tests play, so it describes What (the contract) and is always welcome. Do not apply "comments only hold Why not" to documentation comments. See [docc-symbol-docs.md](docc-symbol-docs.md).

## Comments to avoid

| Avoid | Instead |
|---|---|
| Restating the code: `count += 1 // Increment count` | Delete it. |
| Compensating for a vague name: `let n: Node // best candidate so far` | Rename: `let bestCandidate: Node`. |
| Narrating steps of a long function: `// Step 2: validate input` | Extract `validate(_:)` and let the name speak. |
| Change history: `// 2025-03: changed to use async` | Commit message. |
| Commented-out code | Delete it; version control keeps it. |
| Cryptic notes only the author understands | Rewrite in full sentences, or delete. |

## Good Why not comments in Swift

A good Why not comment has three parts: the alternative not taken, the reason, and the condition under which the reason stops holding. The third part lets a later reader delete the comment and change the code with confidence.

Deliberately unoptimized code:

```swift
// Not using a Set: `tags` has at most 5 elements (limited by the UI), so a
// linear search is fast enough and keeps the declared order.
// Revisit if the limit is raised above about 100.
if tags.contains(newTag) { return }
```

A workaround for an external constraint:

```swift
// Not using `Date.FormatStyle`: the server expects a fixed `en_US_POSIX`
// format regardless of the user's locale (API spec v2, section 4.1).
let formatter = DateFormatter()
formatter.locale = Locale(identifier: "en_US_POSIX")
```

A rejected refactoring:

```swift
// Kept as a `switch` instead of protocol dispatch: the cases must stay
// exhaustive so the compiler flags new `PaymentMethod` cases here.
// Tried in #123 and reverted.
switch method {
```

Code that looks redundant but isn't:

```swift
// Not `[weak self]`: the operation must finish even if the view controller is
// dismissed, and the closure is released when the task completes.
Task { await self.save() }
```

Keep each example's facts true for the code at hand: never invent a measurement, spec section or issue number. If the reason isn't known, ask the user.

## TODO and FIXME

- `// TODO:` reserves future work; a Why not records a decision not to do something. Keep them distinct so TODOs can be reviewed as a list.
- `// FIXME:` marks a known defect left in place.
- Attach an issue ID or URL when one exists (`// TODO(#123): …`). A TODO is not a promise; state the triggering condition or date when "later" is meant.
- Swift also supports `#warning("…")` for a TODO the compiler should surface; use it only if the project already does.

## MARK comments

`// MARK: - Section` organizes a file for Xcode's jump bar. It is navigation, not explanation; follow the file's existing MARK layout and don't add MARKs to files that don't use them.
