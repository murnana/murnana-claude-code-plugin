---
name: test-case
description: Write, add or review Python unit tests (pytest, unittest), one behavior per test, each seen failing once. Not for running an existing suite, fixing production code, or CI setup.
argument-hint: "[file, class or function to test, or the behavior to specify]"
allowed-tools: Read Grep Glob Edit Write AskUserQuestion Bash(python3 -m pytest *) Bash(python -m pytest *) Bash(pytest *) Bash(python3 -m unittest *) Bash(python -m unittest *) Bash(git status *) Bash(git diff *)
---

# Python Test Case

Write Python tests that state **what** the code must do, so that a failing test tells the reader which behavior broke.

- **What a test is for**: t_wada's principle 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」. A test is a readable, executable statement of one behavior.
- **How the work proceeds**: Kent Beck's "Canon TDD" (Japanese translation by t_wada: 「テスト駆動開発の定義」): write a test list, turn exactly one item into a test, make it pass, optionally refactor, repeat.

Read [references/test-design.md](references/test-design.md) before Step 3: it holds the ways to find test cases and the table of test smells used in Step 5. Ask the user questions in Japanese. Write test names, messages and comments in the language the existing tests use; if there are none, use English.

## Hard rules

Follow these in every step. When a step seems to conflict with one, the rule wins.

1. **Test behavior, not implementation.** Assert on what a caller can observe: return values, raised errors, public state, and messages sent across a boundary (a saved record, a sent mail). Never assert on private members, on the order of internal helper calls, or by repeating the implementation's formula in the test.
2. **Expected values come from the specification, never from running the code.** A specification source is: the user's request, a doc comment or document, an issue, an existing test, or a caller that depends on the behavior. Work the expected value out by hand and write it as a literal. If the only way to get it is to run the code, that test is a characterization test: allowed in Mode C only, and labeled as one.
3. **One list item at a time.** Never turn the whole test list into tests in one go: what you learn from one test changes the next. Mode A: exactly one test, then run. Modes B and C: at most 5 tests, then run.
4. **See every new test fail once, for the reason you expect.** A test that has never failed has not shown it can fail. Mode A: it fails because the behavior does not exist yet. Modes B and C: use the failure check in Step 4. Never break production code to make a test fail.
5. **Never bend a test to get green.** Do not delete an assertion, loosen an expected value, add a skip/ignore marker, a retry or a sleep, or change the expected value to what the code returns. A test that states the specification and fails against existing code is a finding: handle it by Step 4's "the code looks wrong" branch.
6. **Change test code only**, unless the user asked you to implement or fix the behavior (Mode A with implementation). Test code means test files, test fixtures and helpers, and the one build entry that registers a new test file. Changes to production code that would make it testable are proposals for the report.
7. **No logic in tests.** No `if`, loops or `try/catch` that decide what is asserted, and no computed expected values. Several inputs for one behavior become a parameterized test. Each test builds its own data, leaves nothing behind, and passes when run alone or in any order. No real clock, randomness, network, or files outside a temporary directory, and no sleeping.
8. **If you cannot ask** (no `AskUserQuestion` tool, a non-interactive run, or the user said they are away), don't stop and don't guess silently: take the default the step names, mark the item `assumed` in the test list, and list it in the report.

## Working efficiently

- Use Bash only for the test commands in "Python specifics" and the `git` commands written here, exactly as written, one command per call: no shell variables, `;`, `&&`, pipes or `cd`. Other forms don't match the pre-approved tools and trigger a permission prompt. List files with Glob, search with Grep, read with Read.
- Do not install a framework, plugin or dependency, and do not create a test project. If something needed is missing, or a test command is denied, write the tests anyway, say they were not run, and name what is missing.
- Never report a test as passing, or as seen failing, unless you ran it and read the output. "0 tests run" is not a pass.
- Code pasted into the conversation instead of a file: skip the commands, apply every other step to the pasted code, reply with the full test file, and write 「未実行」 under 実行結果.

## Step 1: Fix the scope and the mode

1. Target = `$ARGUMENTS` (a file, class, function, or a behavior in words). If empty, take it from the conversation. If there is none, ask.
2. Choose the mode. Take the **first** row that matches, and say which mode you chose in your reply:

   | Mode | When | What you may change |
   |---|---|---|
   | **A. Test-first** | The behavior does not exist yet, the user asks for TDD, or the user reports a bug to fix. For a bug, the first test reproduces the bug. | Tests. Production code only if the user asked you to implement or fix it. |
   | **C. Characterization** | The code exists, no specification can be found, and the user wants to pin the current behavior before changing it (refactoring, migration, legacy code). | Tests only. |
   | **B. Test-after** | The code exists and its specification can be found. This is the default when unsure. | Tests only. |

3. Find the framework and conventions with the detection steps in "Python specifics". Project instructions (`CLAUDE.md`, `.claude/rules/`, `CONTRIBUTING.md`) override this skill.
4. Read the one or two existing test files closest to the target, and imitate them: file location, naming, assertion style, fixtures, the language of test names.
5. Run the existing tests for the target area once ("Run the file" command) and record the result as the baseline.
   - Passes → continue.
   - Fails before you changed anything → record which tests fail, do not fix them, continue.
   - Cannot run (tool missing, build broken) → continue, and report every later run as 「未実行」 with the error's first lines.

## Step 2: Understand the contract

1. Read the target once, its doc comments, and two or three call sites (Grep for the name). Do not read every caller.
2. Write down, for each public entry point in scope: inputs and their valid ranges, outputs, errors, side effects, and state it keeps.
3. List the dependencies a test cannot control: current time, randomness, network, database, filesystem, environment variables, global or static state, threads.
4. For each such dependency, decide in this order:
   1. The code already accepts it as a parameter or constructor argument → pass a fixed value or a hand-written fake.
   2. The framework has a supported way to replace it (see "Python specifics") → use that, and restore it after the test.
   3. Neither → do not reach in with reflection, private access or global patching. Test what can be tested, and put a proposal in the report: the smallest change that lets the dependency be passed in.

## Step 3: Write the test list

Write the list in your reply **before any test code**, using [references/test-design.md](references/test-design.md) to find the cases:

```
Test list: <target> (Mode <A/B/C>)
- [ ] <condition> → <expected result> | normal / boundary / error / state | source: <where the expected result comes from>
```

1. One line per behavior, in words a user of the code would use. "returns 0 when the subtotal is exactly 5000", not "covers the else branch".
2. Derive the lines from the contract in Step 2, not from the branches of the implementation. Then read the implementation once more only to find inputs the contract forgot (a special case, an early return) and ask what the specification says about them.
3. Leave off: private functions, trivial accessors, behavior of the language, the framework or a library, and anything the type system already guarantees.
4. Mark a line `[x] existing: <test name>` when an existing test already states it. Do not write it again.
5. Order: the simplest normal case first, then boundaries, then errors, then state and combinations.
6. A line whose expected result has no source gets `?`. Batch all `?` lines into one `AskUserQuestion` call (up to 4 questions; show the input and the candidate results as options, and include 「現在の動作を仕様とする」 when the code exists). If there are more than 4, ask the 4 that change the most tests and treat the rest by rule 8, whose default is: leave the line untested and report it.
7. In Mode C the source of every line is `current behavior`. Say so once above the list.

The list is a working document: when writing a test shows a new case, add a line instead of handling it at once.

## Step 4: Turn the list into tests

Take the lines in order. For each line:

1. **Name** the test so that it states the condition and the expected result (naming row in "Python specifics"). A reader should learn the behavior from the list of test names alone. Never `test1`, `testShippingFee`, `works`, `正常系`.
2. **Write the assertion first**, then the call that produces the value, then the setup the call needs. Lay the test out as Arrange, Act, Assert, separated by blank lines, with exactly one Act. When there is nothing to arrange, a single line that calls and asserts is fine.
3. **One behavior per test.** Several assertions are fine when they describe one result (the fields of one returned object). A second Act, or assertions about a different behavior, means a second test.
4. **Data**: use the smallest input that shows the behavior, and write the values that matter in the test itself. Put values that do not matter behind a helper or builder with defaults. No value shared through a mutable global.
5. **Test doubles**: use the real collaborator when it is fast and deterministic. Replace only the dependencies listed in Step 2, with a hand-written fake or stub first. Verify that a call happened only when the call is the behavior (the mail was sent). Never replace the unit under test or part of it.
6. **Run** it with the "Run one test" command and read the output:

   | Mode | Result | Do |
   |---|---|---|
   | A | Fails, and the message shows the missing behavior | This is the expected red. If you may implement: write the least production code that passes this test and every earlier one, run the file, then refactor only while everything passes, and add any new case you noticed to the list. If you may not: leave the test red and say so in the report. |
   | A | Passes at once | The behavior already exists or the test checks nothing. Do the failure check below; if it holds, mark the line `[x] already satisfied` and treat the target as Mode B from here. |
   | A | Fails for another reason (syntax, import, wrong setup) | Fix the test and run again. |
   | B, C | Passes | Do the failure check below. |
   | B | Fails | Read the source of the expected value again. The test misreads the specification → fix the test. The test is right → "the code looks wrong" below. |
   | C | Fails | The expected value was copied wrongly; correct it from the actual output and run again. |

7. **Failure check** (Modes B and C, and Mode A tests that passed at once): change the expected value in the test to a wrong one (or, for an expected error, an input that does not raise), run the test, and confirm that it fails and that the message shows both the expected and the actual value. Restore the test and run it again to confirm it passes. Do this for every test; for a parameterized test, once per test function. If the test still passes with the wrong value, the assertion is not being executed: fix the test.
8. **The code looks wrong** (Mode B, the test states the specification and the code does something else): do not change the expected value and do not change the code. Ask, together with any other open question, which holds: 「コードの不具合(テストを残し、修正は別途)」, 「現在の動作が仕様(テストを直す)」 or 「このテストは書かない」. If you cannot ask: delete the test from the test file (do not park it in another file), and put its full code, the expected and actual values and the specification source in the report, so the suite stays green and the finding is not lost.
9. Tick the line in the test list.

## Step 5: Verify

Run each check, fix what your tests caused, and re-run until clean, at most 3 rounds:

1. Run the whole test file, then the suite it belongs to ("Run the file / all" commands). Every test passes, except the Mode A tests you reported as red and the failures recorded in Step 1's baseline.
2. Run the test file a second time. A different result means a test depends on order, time or shared state: find the cause with rule 7. Do not add a retry.
3. Run `git status --short`. Outside Mode A with implementation, only test code may be listed (rule 6). Undo anything else, and delete any scratch or temporary file you created.
4. Read every test you wrote against the smell table in [references/test-design.md](references/test-design.md), and answer for each test: Would it still pass if the implementation were rewritten without changing behavior? Would it fail if the behavior in its name broke? Does its failure message say what was expected and what happened?
5. Confirm every line of the test list is ticked, or listed in the report with the reason it was left.

## Step 6: Report

Reply in Japanese with exactly these headings, writing 「なし」 under an empty one:

```
## モードと前提
## テストリスト
## 書いたテスト
## 失敗の確認
## 見つかった問題
## 提案(未適用)
## 実行結果
```

- モードと前提: the mode, the framework, the baseline from Step 1, and every `assumed` item.
- テストリスト: the final list with its ticks, including lines left untested and why.
- 書いたテスト: `file` and test name, one line each, in the order of the list.
- 失敗の確認: how each test was seen failing (Mode A red, or the failure check), or 「未実行」.
- 見つかった問題: suspected bugs (expected, actual, specification source, and the test code if it was taken out), and specification gaps with the question to answer.
- 提案(未適用): changes to production code that would make it testable, and refactorings. Not applied.
- 実行結果: each command you ran with its outcome (for example `12 passed`), or 「未実行」 with the reason.

Do not commit unless the user asks.

## Python specifics

### Detect the framework

1. Glob `pyproject.toml`, `pytest.ini`, `setup.cfg`, `tox.ini`, `conftest.py`, and Grep the existing tests for `import pytest` and `unittest.TestCase`.
2. pytest settings, a `conftest.py` or `import pytest` in tests → **pytest**. Only `unittest.TestCase` → **unittest**. No tests at all → pytest if `pytest` is in the project's dependencies, otherwise unittest (standard library; nothing to install).

### Conventions and commands

| Topic | Use |
|---|---|
| Test file | Next to the existing tests; otherwise `tests/test_<module>.py`. Test functions `test_<behavior>`. |
| Test name | `test_<condition>_<expected result>` in snake_case, e.g. `test_subtotal_at_threshold_ships_free`. Non-ASCII names are legal; use them only if the existing tests do. |
| Run one test | `python3 -m pytest <file>::<test_name> -q` (unittest: `python3 -m unittest <package.module.Class.test_name> -v`) |
| Run the file / all | `python3 -m pytest <file> -q` / `python3 -m pytest -q` (unittest: `python3 -m unittest discover -v`) |
| Many inputs, one behavior | `@pytest.mark.parametrize` with `ids=` or `pytest.param(..., id="...")` so each case has a name (unittest: `self.subTest(...)`). |
| Expected error | `with pytest.raises(ValueError, match="..."):` around the Act line only (unittest: `self.assertRaises`). |
| Floats | `pytest.approx(...)`, never `==`. |
| Time, randomness, environment | Pass the clock or `random.Random(seed)` in as an argument when the code allows it; otherwise `monkeypatch.setattr` / `monkeypatch.setenv`. Files go in the `tmp_path` fixture. |
| Async code | Use the project's plugin (`pytest-asyncio`, `anyio`). If none is installed, do not add one; report it. |

### Example

```python
import pytest

from shop.shipping import shipping_fee


def test_subtotal_below_threshold_costs_flat_fee():
    fee = shipping_fee(subtotal=4999)

    assert fee == 500


@pytest.mark.parametrize(
    ("subtotal", "expected"),
    [
        pytest.param(5000, 0, id="exactly at the threshold"),
        pytest.param(5001, 0, id="just above the threshold"),
    ],
)
def test_subtotal_at_or_above_threshold_ships_free(subtotal, expected):
    assert shipping_fee(subtotal=subtotal) == expected


def test_negative_subtotal_is_rejected():
    with pytest.raises(ValueError):
        shipping_fee(subtotal=-1)
```

The three boundary values in the example (4999, 5000, 5001) come from the specification "5000 or more ships free", not from reading the comparison operator in the code.

## Gotchas

- A plain `assert` gives a readable diff only under pytest's assertion rewriting. In helper modules outside the test files, call `pytest.register_assert_rewrite` or keep asserts inside the tests.
- `unittest.mock.patch` must target the name where it is looked up (`shop.shipping.requests`), not where it is defined. Prefer `autospec=True` so a wrong signature fails.
- A fixture with `scope="module"` or `"session"` that returns a mutable object is shared state. Keep function scope unless setup is slow and the object is read-only.
- Do not put assertions inside `pytest.raises` after the raising line: they never run.
