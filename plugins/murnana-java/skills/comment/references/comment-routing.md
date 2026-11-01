# Routing Information: How, What, Why, Why not

Rules for implementation comments (`//`, `/* ... */`) and for deciding what belongs in a comment at all. Doc comments (`/** ... */`) follow [javadoc.md](javadoc.md).

Basis: Takuto Wada (t_wada)'s principle, posted on 2017-09-05 (https://x.com/t_wada/status/904916106153828352): code holds How, test code holds What, the commit log holds Why, and code comments hold Why not. In his follow-up reply, "Why not" means why another approach was not taken, that is, what was deliberately not done. Some call it the HWWWn principle. It is a mnemonic, not a strict law; he later wrote of leaving Why and Why not in commit logs *or* comments. This file supplements it with John Ousterhout's point (*A Philosophy of Software Design*, "Comments belong in the code, not the commit log") that a reason every reader of the line needs must also be in the code.

## Contents

1. Routing table
2. Why each place
3. Write a "Why not" comment
4. Keep an essential "Why" in the code
5. TODO, FIXME and similar markers
6. Comments to delete or rewrite
7. Commit messages and tests proposed alongside
8. Examples

## 1. Routing table

| Information | Put it in | Not in a comment because |
|---|---|---|
| **How** it works | The code: names, extracted methods, explaining variables, types | Code is what runs, so it can't go stale; a comment that repeats it can |
| **What** it must do (behavior spec) | Tests, with test names that read as the spec | A passing test is a spec that is checked on every build |
| **What** callers may rely on (API contract) | The doc comment | This is the reader-facing spec of an API; see [javadoc.md](javadoc.md) |
| **Why** the change was made | The commit message (body, after a blank line) | It is context of the change, tied to the diff and found with `git blame` |
| **Why not**: rejected alternatives, deliberate non-optimizations, workarounds, kept "ugly" code | An implementation comment next to the code | The code shows only what was done; what was not done is visible nowhere else |
| **Why** every reader of this line must know (non-obvious constraint, external spec, unusual idiom) | An implementation comment, even if the commit also says it | Readers rarely search the commit log; the reason must sit where the code is read |
| Work not yet done | `TODO` with an owner or issue ID (section 5) | — |

Decision order for a candidate comment:

1. Can the code say it (rename, extract, explaining variable, a type, an assertion)? → Change the code (or, if code changes are out of scope, propose it) and drop the comment.
2. Is it a behavior rule? → A test (propose one if missing). If it is part of the public API contract, also the doc comment.
3. Is it the story of a change (bug report, review request, what changed)? → The commit message.
4. Is it something deliberately not done, or a reason a future editor would otherwise undo? → A comment.
5. Otherwise, write no comment.

## 2. Why each place

- Misplaced information decays: How in a comment drifts from the code (comment rot); Why only in a reviewer's head is lost; a spec only in prose is never checked.
- A reader who sees odd code assumes the author didn't know better. Without a "Why not" comment, the next editor "simplifies" it, breaks something, and reverts: the same failed refactoring repeats years later.
- An identifier can carry one idea. It can say what a function does, not which trade-off it makes; the trade-off needs a comment.

## 3. Write a "Why not" comment

Write one when the code looks improvable and the obvious improvement is wrong, or was tried and abandoned:

- A seemingly redundant check or step that a known case requires.
- An optimization deliberately not done (input is small, measured to be fast enough).
- A newer API or library deliberately not used (environment, compatibility, licensing).
- A workaround for a bug or quirk in a dependency, JVM, OS or external service.
- A refactoring that was tried and rejected (the polymorphic version breaks a rule; the stream version was slower in a measured hot path).
- A design alternative rejected (a lock-free structure, a cache, a different data type).

A good one contains:

1. **The rejected option**, named specifically ("a `HashMap` keyed by id", "`String#isBlank()`"), not "other ways".
2. **The reason**: the constraint, measurement, spec, or bug, with a link or issue ID when one exists.
3. **When it stops holding**: the condition under which the comment and code can be revisited ("if a batch exceeds a few thousand rows", "once the minimum JDK is 11", "when LIB-1234 is fixed"). This lets a later reader delete it with confidence.

Keep it short (one to four lines), place it directly above the code it protects, and write it so the person who deletes it later understands exactly what to check.

## 4. Keep an essential "Why" in the code

The principle sends the Why of a change to the commit log. Keep a Why in a comment too when it explains the code as it stands, not the change:

- A link to an external specification the code implements (RFC, file format, vendor API doc), with the section.
- A unit, range or invariant not expressible in the type.
- An idiom unusual for Java or for this codebase.
- Code copied or adapted from elsewhere: the source URL (and check its license).
- A bug fix whose reason is invisible in the fixed code and that a future change could easily reintroduce.

Test: "Would someone editing this line, who never reads `git log`, make a mistake without this sentence?" If yes, it stays in the code.

## 5. TODO, FIXME and similar markers

- `TODO(owner or ISSUE-ID): what remains, and the condition or date it depends on`. Use the project's existing marker style if it has one.
- `FIXME(...)`: known defect left in place. `HACK` / `XXX`: use only if the project already does; a "Why not" comment is usually clearer.
- A TODO is not a promise. Prefer a ticket in the issue tracker, referenced from the comment, over a TODO with no owner.
- A TODO reserves future work; a "Why not" records a decision not to do it. Don't write a "Why not" as a TODO, or the next reader will try to "finish" it.

## 6. Comments to delete or rewrite

| Found | Action |
|---|---|
| Restates the code (`i++; // increment i`) | Delete |
| Explains a vague name (`Node n; // best candidate`) | Rename (or propose renaming) and delete |
| Narrates steps of a long method (`// step 1: validate`) | Extract methods named after the steps (or propose it); delete |
| Change history, author or date (`// 2024-03 fixed by X`) | Delete; it belongs in the commit log |
| Commented-out code | Delete; VCS keeps it. If it must stay, add a "Why not" saying why and until when |
| Closing-brace labels (`} // end if`) | Delete; shorten the block instead |
| Contradicts the code | Find out which is right; fix the code or the comment; never leave both |
| Cryptic note only the author understood | Rewrite with the rejected option and reason, or delete |
| `/** */` on a private member, used as a note | Turn into a `//` comment, unless the project documents private members |
| A spec rule stated only in a comment | Propose a test; keep a short pointer if useful |

Don't delete a comment whose purpose you can't determine; ask the user, or list it as a question in the report.

## 7. Commit messages and tests proposed alongside

When information moves out of a comment, don't drop it; hand it to the user as a proposal:

- **Commit message**: a summary line, a blank line, then the Why: the problem, the constraint, the reason for this approach. Not "applied review comments", but why the change was needed. Follow the repository's commit message rules.
- **Test**: a test name that reads as the rule (`returnsEmptyWhenKeyExpired`, or the project's naming style) and the case it covers.
- **Code change**: the new name or extracted method, and the comment it replaces.

## 8. Examples

Redundant-looking check (Why not):

```java
// Don't reduce this to `value == null`: JSONObject.NULL is a non-null
// sentinel whose equals(null) returns true, and callers expect null.
if (value == null || value.equals(null)) {
    return null;
}
```

Deliberately unoptimized (Why not, with an expiry condition):

```java
// A nested loop instead of a HashMap index: both lists come from one
// settings screen and stay under 50 items, and the map costs more to
// build than the loop. Revisit if this is ever called with bulk data.
for (Rule rule : rules) {
    for (Target target : targets) { ... }
}
```

Newer API not used (Why not):

```java
// Not String#isBlank(): this module still targets Java 8 (see pom.xml
// maven.compiler.release). Switch once the minimum JDK is 11.
if (s.trim().isEmpty()) { ... }
```

External spec (essential Why):

```java
// RFC 4180 section 2: records end with CRLF, regardless of platform.
out.append("\r\n");
```

Rejected refactoring:

```java
// Kept as a switch on purpose: replacing it with per-type subclasses was
// tried (PR #812) and breaks the rule that discounts stack across types.
switch (type) { ... }
```

Workaround with a removal trigger:

```java
// Workaround for LIB-1234: the driver ignores the fetch size unless
// autocommit is off. Remove when the driver is upgraded past 42.7.
connection.setAutoCommit(false);
```

Before and after (How moved into code):

```java
// Before
// check whether the user can edit: admin, or owner and not locked
if (u.role == ADMIN || (doc.ownerId == u.id && !doc.locked)) { ... }

// After (proposed): the name carries the How, no comment needed
if (canEdit(user, document)) { ... }
```
