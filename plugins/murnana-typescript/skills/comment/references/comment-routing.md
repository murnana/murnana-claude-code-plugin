# Routing Information: How, What, Why, Why not

Rules for implementation comments (`//`, `/* ... */`) and for deciding what belongs in a comment at all. Doc comments (`/** ... */`) follow [tsdoc.md](tsdoc.md).

Sources (ideas summarized in our own words; no text reproduced):

- Takuto Wada (t_wada), post on X, 2017-09-05, https://x.com/t_wada/status/904916106153828352, and his reply in the same thread defining "why not" as the reason a different approach was not adopted.
- John Ousterhout, *A Philosophy of Software Design*, ch. 13 and §16.3 ("Comments belong in the code, not the commit log").
- Ellen Spertus, "Best practices for writing code comments", Stack Overflow Blog, 2021-12-23.
- Joshua Bloch, *Effective Java*, "Write doc comments for all exposed API elements" (doc comment = contract with the client).

## The rule

Each place in a project records a different question about the software:

| Place | Records | Checked by |
|---|---|---|
| Code | **How**: the procedure that makes it work | The compiler and the tests |
| Test code | **What**: the behavior it must have (an executable specification) | Running the tests |
| Commit log | **Why**: the reason a change was made at that moment | Review, `git blame` |
| Code comment | **Why not**: what was deliberately *not* done, and why | Nothing — so keep it short and rare |

t_wada's own gloss: write in comments the things you chose not to do, for the next person and your future self. What the code does can be made clear without comments; what it deliberately does not do has no other place to become visible.

Treat the split as a mnemonic, not a law. t_wada himself called the mapping a little forced, and later wrote of leaving both Why and Why not "in the commit log or code comments".

Decision order for a candidate comment:

1. Can the code say it (rename, extract a function, an explaining variable, a narrower type, a union, `satisfies`, an assertion)? → Propose the code change and drop the comment.
2. Is it a behavior rule? → A test (propose one if missing). If it is part of an exported API's contract, also the doc comment.
3. Is it the story of a change (bug report, review request, what changed)? → The commit message.
4. Is it something deliberately not done, or a reason a future editor would otherwise undo? → A `//` comment.
5. Otherwise, write no comment.

## Why this split works

- **Avoid duplication.** A comment that repeats the code or tests is an unverified second copy. It drifts and starts lying (comment rot).
- **Each kind of knowledge has a natural lifetime.**
  - How changes with every refactor, so it lives in the code. Wanting to explain How in a comment is a signal to rename or restructure.
  - What changes only when requirements change and must be checked automatically: tests. Test names should read as the specification.
  - Why belongs to the moment of a change (the bug, the request, the constraint). `git blame` connects it to the lines.
  - Why not belongs to the *current* shape of the code: it answers the question a reader asks at this line ("why not just use X?"), and stops the next person from "simplifying" it back into a bug or retrying a refactor that already failed.
- **Comments are not executed.** Put in them only what has no better home.

## Refinement: essential Why also goes in the code

Developers rarely search the commit log while reading code, and commit messages tend to be short and get buried by later commits. So if a reason is something anyone *touching this line* must know (a non-obvious constraint, a dependency on an outside fact), write it in a comment as well, even though the commit message also has it. History and the story of the change ("changed on …", "added for #12 by …", "fixed review comment") stay in the commit only.

## What a good "why not" comment contains

1. **The alternative not taken**, concretely (`Promise.all`, a `Map`, the polymorphic version).
2. **The reason**: the constraint, measurement, spec clause or bug that rules it out, with a link if there is one.
3. **The condition under which the reason stops holding** ("revisit if the list exceeds a few hundred items", "remove when Safari 15.3 support ends").

Point 3 lets a future reader delete the comment and the workaround safely once the premise is gone. Write the comment so it is easy to remove.

Typical cases:

- A choice that looks redundant or naive but is required (a check that looks like it can be simplified).
- An optimization deliberately not done, with the data size or measurement that justifies it.
- A newer API not used because of an environment constraint.
- A workaround for an outside bug or quirk.
- A behavior dictated by an external spec (link the RFC or spec section).
- A refactoring that was tried and abandoned, and why it failed.

## TODO and friends

- A TODO reserves future work; a "why not" records a decision not to do something. Keep them distinct.
- Write a TODO with an issue ID or owner and a concrete trigger or date: `// TODO(#123): drop this branch when the v1 API is retired`. A TODO is not a promise; one with no reference or condition is noise.
- Use the project's existing markers (`TODO`, `FIXME` for a known defect, `HACK` for an inelegant workaround, `XXX` for a serious hazard). Do not introduce new marker styles.

## Tool directives

`// @ts-expect-error`, `// @ts-ignore`, `// eslint-disable-next-line`, `// prettier-ignore`, `/// <reference>`, `/* #__PURE__ */` and similar comments are instructions to a tool, not prose. They apply to the next line (or the next expression), so moving, rewording or deleting one changes behavior.

- Never move or edit them. `ts_comments.py check` fails if one moves or changes.
- A directive with no reason is a classic "Why not": why the type error or lint rule is not fixed. Write the reason on a `//` line **above** the directive (never between the directive and its code), from evidence, with the condition for removing it:

  ```ts
  // The upstream typings mark `opts` as required, but the API accepts undefined (lib#812).
  // Remove when @acme/client >= 3.2 is the minimum.
  // @ts-expect-error
  client.connect(undefined);
  ```

- `@ts-expect-error` vs `@ts-ignore`, or an inline description after the directive (`// @ts-expect-error -- reason`), are code-level changes: propose them, don't make them.

## Doc comments are a separate category

The rule targets **implementation comments** inside the code. **Doc comments** on exported API (TSDoc) are different: they are the contract a caller reads in editor hovers and generated docs without the body or tests in view. A doc comment describes *what* the declaration does for its client — meaning, units, ranges, errors, side effects — independent of the implementation, never *how* it does it. Applying "comments contain only Why not" to doc comments is a misuse of the rule. The tests still verify the contract. How to write them: [tsdoc.md](tsdoc.md).

## Applying it to TypeScript

- TypeScript types already state much of the What at the signature (parameter and return types, nullability, `readonly`). Do not repeat types in prose, in doc comments or inline.
- Inside function bodies, comment Why not (and essential Why), not How.

## Examples

```ts
// Bad (How): repeats the code
// Loop over users and keep the active ones
const active = users.filter((u) => u.active);

// Bad (history, belongs in the commit)
// 2024-03-01: switched to filter because of review comment

// Good (Why not): explains a choice that looks wrong
// Not `await Promise.all(...)`: the API rate-limits us to one request at a time.
for (const id of ids) {
  await fetchUser(id);
}

// Good (Why not + reason + removal condition)
// setTimeout(0) instead of queueMicrotask: Safari < 15.4 has no queueMicrotask.
// Remove when Safari 15.3 support ends.
setTimeout(flush, 0);

// Good (deliberately unoptimized, with the premise)
// O(n^2) on purpose: n is the number of tabs (< 50), and a Map-based
// version made the ordering logic much harder to follow. Revisit if n grows.
for (const a of tabs) for (const b of tabs) { /* ... */ }

// Good (abandoned refactoring)
// Kept as a switch: replacing it with a strategy map broke the fallthrough
// required by the legacy import format (see #842).
```
