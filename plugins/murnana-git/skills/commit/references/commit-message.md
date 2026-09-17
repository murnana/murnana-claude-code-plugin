# Fallback commit convention

Apply this convention **only when [project-rules.md](project-rules.md) finds no
project-specific rule.** It is based on Takuto Wada (t_wada)'s principle:

> コードには How / テストコードには What / コミットログには Why / コードコメントには Why not
> (Code: How / Tests: What / Commit log: Why / Code comments: Why not)
> — <https://x.com/t_wada/status/904916106153828352>

Code only ever shows its current shape, so the commit log is the only place that
can preserve *why* a change was made — the problem it solved, the constraint it
satisfied, the reasoning behind the decision. The diff itself already shows the
What/How, so repeating that in the log adds almost no information.

## Format

```
:emoji: Short, concise title (~50 chars)

Why this change was needed: the problem solved, the constraint satisfied, or the
reasoning behind the decision. Do not restate the How — that's visible in the diff.

Refs: #123
```

- The title starts with a GitHub emoji markup code (e.g. `:memo:`).
- The body is optional, but **required whenever the Why is not obvious** from the
  title or diff alone.

## Emoji table (gitmoji-based)

| Emoji | Use |
|---|---|
| `:sparkles:` | New feature |
| `:bug:` | Bug fix |
| `:recycle:` | Refactor |
| `:memo:` | Documentation |
| `:white_check_mark:` | Tests |
| `:art:` | Formatting / structural improvement |
| `:zap:` | Performance |
| `:fire:` | Removal |
| `:wrench:` | Configuration |
| `:arrow_up:` | Dependency update |
| `:bookmark:` | Version bump |
| `:construction:` | Work in progress |
| `:green_heart:` | CI fix |

## Why: good vs. bad examples

- Bad: `:memo: READMEを更新` — restates only the What, which the diff already shows.
- Good: `:memo: インストール手順にマーケットプレイス追加の前提を追記`
  with body: 「先に marketplace add をしていないと install が失敗するという問い合わせが
  複数あったため」— states the motivating problem.

## Splitting: good vs. bad examples

- Bad: bundling a bug fix, a variable rename, and a dependency bump into one commit.
- Good: three commits, one per why — each can be reverted or bisected independently.
