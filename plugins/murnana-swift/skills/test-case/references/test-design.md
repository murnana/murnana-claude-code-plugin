# Test design

How to find the cases for a test list, and how to recognize a test that will not earn its keep. Language-independent; the framework syntax is in SKILL.md.

## Contents

- Finding cases
- Choosing the next test (Mode A)
- Test size
- Test doubles
- Characterization tests (Mode C)
- Test smells
- Sources

## Finding cases

Work through these in order for each public entry point. Each one adds lines to the test list.

| Technique | Ask | Lines it adds |
|---|---|---|
| Equivalence classes | Which groups of inputs are treated the same way by the specification? | One representative per group, valid and invalid. Not several values from the same group. |
| Boundaries | Where does one group end and the next begin? | For a limit `n` stated as "n or more": `n-1`, `n`, and `n+1`. For a range: just below the minimum, the minimum, the maximum, just above the maximum. |
| Zero, one, many | What happens with nothing, with exactly one, with several? | Empty collection or string, one element, two or more; first and last position. |
| Absent values | Can an input be null, missing, blank, or the default? | One line per absent input the contract allows or rejects. |
| Errors | Which inputs or states must be rejected, and how? | One line per documented error, asserting its kind and what the caller needs from it (not the full message text unless it is part of the contract). |
| State | Does the result depend on what happened before? | One line per transition that matters, including the forbidden ones (close twice, use after close). |
| Combinations | Do two conditions interact? | A small decision table: one line per rule in the specification, not every combination. |
| Round trips and invariants | Is there a property that always holds (parse then format gives the input back; the total never goes negative)? | One line per property, with concrete examples; a property-based test only if the project already uses such a library. |
| Regressions | Is there a reported bug? | One line that reproduces it, named after the behavior, not the ticket number. |

Stop adding lines when a new line would fail for the same reason as an existing one. More tests of the same equivalence class add run time and maintenance, not confidence.

## Choosing the next test (Mode A)

Pick the line that teaches the most for the smallest step:

1. Start with the simplest normal case, even if its first implementation is a constant (fake it).
2. Add a second example that forces the constant to become real logic (triangulate).
3. When the implementation is obvious, write it directly; if a test then surprises you, go back to smaller steps.
4. Refactor only while every test passes, and never in the same step as making a test pass.

## Test size

Classify by what a test touches, not by the words "unit" or "integration":

| Size | Touches | Use for |
|---|---|---|
| Small | Only memory, in one process: no network, database, filesystem, clock or sleep | Almost everything. The default. |
| Medium | localhost only: a real database, the filesystem, another process | The code whose job is that boundary (a repository, a file parser). |
| Large | Other machines or external services | Only where the project already has such tests. Do not add them here. |

Many small tests, fewer medium, very few large. If a behavior can be stated as a small test, do not state it as a larger one.

## Test doubles

| Kind | What it does | Use when |
|---|---|---|
| Dummy | Fills a parameter and is never used | The parameter is irrelevant to the behavior |
| Stub | Returns fixed answers | The test needs the dependency to say something specific |
| Fake | A working, simplified implementation (in-memory repository, fixed clock) | The dependency is slow or nondeterministic and the test needs it to behave |
| Spy | Records how it was called, checked afterwards | The outgoing call is the behavior |
| Mock | Is told beforehand which calls to expect | Same as a spy; prefer a spy, whose assertion sits in the Assert section |

Rules of thumb: replace only what you cannot control (Step 2's list). Do not replace value objects or types the project does not own; wrap those in a thin adapter the project owns and replace the adapter. A test with more double setup than assertions is testing the doubles.

## Characterization tests (Mode C)

A characterization test records what the code does now, so that a later change that alters it is noticed. It does not say the behavior is right.

1. Write the call with an expected value you know is wrong, run it, and read the actual value from the failure message.
2. Put the actual value in as the expected value, and run again to see it pass.
3. Name or tag the test so that a reader knows it pins current behavior (for example a "characterization" group, suite or comment in the form the project's tests use).
4. If the recorded value looks like a bug, keep the test, and report it: the user decides whether it is a bug before anything is changed.

Choose inputs with "Finding cases" all the same; only the source of the expected value differs.

## Test smells

Check every test you wrote against this table in Step 5.

| Smell | Why it hurts | Fix |
|---|---|---|
| No assertion, or only "does not throw" where a result exists | Passes whatever the code does | Assert the result the specification names |
| Expected value computed with the same formula as the code | The test repeats the bug | A literal worked out by hand |
| Expected value copied from the output (outside Mode C) | States what the code does, not what it should do | Take it from the specification; if there is none, ask |
| Name says how or nothing (`test1`, `testCalc`, `callsHelper`) | A failure does not say which behavior broke | Condition and expected result in the name |
| Several behaviors in one test | The first failure hides the rest; the name cannot be accurate | One test per behavior |
| `if`, loop or `try/catch` in the test | The test needs its own tests; a branch can skip the assertion | Parameterized test; the framework's expected-error assertion |
| Asserts on private state or internal call order | Breaks on refactoring that keeps behavior | Assert through the public interface |
| Everything replaced by doubles | Passes while the real parts do not fit together | Real collaborators; doubles only at the uncontrollable edges |
| Depends on the real time, random values, network, or machine settings | Fails some days and on some machines | Pass the value in; fixed clock and seed |
| Depends on another test having run, or on shared mutable fixtures | Fails when run alone or in another order | Each test builds what it needs |
| `sleep` or a retry to wait for something | Slow, and still fails under load | Wait on the result itself (await, future, fake clock) |
| Large setup the reader must scroll past | Hides which input matters | Helper or builder with defaults; only the relevant values in the test |
| Whole-output or snapshot comparison for one fact | Fails on unrelated changes, and failures get approved without reading | Assert the fact |
| Skipped or disabled test without a reason and an owner | Rots; nobody knows whether it should pass | Fix or delete; never add one to get green |
| Test that mirrors the code line by line to raise coverage | Coverage rises, confidence does not | Derive the case from the contract |

## Sources

Ideas summarized in this skill's own words:

- Kent Beck, "Canon TDD" (2023): https://newsletter.kentbeck.com/p/canon-tdd . Japanese translation by Takuto Wada (t_wada), 「【翻訳】テスト駆動開発の定義」: https://t-wada.hatenablog.jp/entry/canon-tdd-by-kent-beck . The test list, one test at a time, and the listed mistakes (tests without assertions, converting the whole list at once, copying actual values into expected values, mixing refactoring into making a test pass).
- Takuto Wada (t_wada), 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」: https://x.com/t_wada/status/904916106153828352 .
- Kent Beck, "Test-Driven Development: By Example" (2002; Japanese edition 『テスト駆動開発』 translated by Takuto Wada, 2017): fake it, triangulate, obvious implementation.
