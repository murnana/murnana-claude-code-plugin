# What to write in a rule, by purpose

## Universal checklist (every rule)

**Frontmatter**
- Scope with `paths` unless the rule truly applies to almost every session (see [rule-vs-alternatives.md](rule-vs-alternatives.md)).
- Patterns quoted, verified to match real files.

**Shape**
- `# <Topic> Rules` heading. Optionally one line saying what the rule covers / when it applies.
- Group related bullets under `##` subheadings once there are more than ~7.
- Imperative bullets. One instruction per bullet.

**Each instruction must be**
- **Concrete and verifiable**: "Use 2-space indentation", not "Format code properly". "API handlers live in `src/api/handlers/`", not "Keep files organized".
- **Non-obvious**: ask "Would removing this cause Claude to make a mistake?" If not, cut it.
- **Justified when the reason isn't self-evident**: `Do X, not Y — Y causes <concrete failure> because <mechanism>.` The *why* lets Claude generalize to cases the rule didn't list.
- **Anchored to the repo**: real commands, real paths, a real example file to imitate (`follow the pattern in src/api/users.ts`).
- **Consistent** with CLAUDE.md, other rules, and user rules — conflicting instructions get resolved arbitrarily.

**Add a short example** (good vs. bad snippet, ≤10 lines) only when the wording alone is ambiguous.

**Emphasis**: at most one `IMPORTANT` per file. Emphasizing many lines makes none stand out.

**Exclude**
- Standard language/framework conventions Claude already follows
- Anything a formatter or linter already enforces automatically
- File-by-file descriptions, directory trees, dependency lists (derivable from code)
- Tutorials, long explanations, full API docs (link instead)
- Frequently changing facts (versions, owners, current priorities)
- Step-by-step procedures (→ skill)
- Prohibitions that must be enforced (→ permission / hook; the rule may explain the why)
- Self-evident advice ("write clean code", "handle errors")

**Size**: well under 200 lines; most good rules are 5–30 lines.

---

## By purpose

### 1. Code style / language conventions

- **paths**: per language, e.g. `"**/*.{ts,tsx}"`, `"**/*.py"`, `"Source/**/*.{h,cpp}"`
- **Write**: only deviations from tool/community defaults — export style (named vs default), naming conventions with concrete casing, import ordering if not auto-sorted, strictness (no `any`, required type hints), error-handling idiom, logging API to use
- **Skip**: anything the formatter/linter fixes; general "readability" advice

### 2. Framework / layer conventions (API, UI components, data access)

- **paths**: the layer's directories, e.g. `"src/api/**/*.ts"`, `"src/components/**/*.tsx"`
- **Write**: required response/error shape, where validation happens and with what, file placement and naming, state-management choice, the canonical example file to imitate, forbidden shortcuts with the why (e.g. "don't call the DB from components — breaks SSR caching")
- **Skip**: framework basics; full endpoint lists

### 3. Testing

- **paths**: test files, e.g. `"**/*.test.{ts,tsx}"`, `"tests/**"`, `"**/*_test.go"`
- **Write**: exact command to run a single test / a file (not just the whole suite), test naming pattern, what to mock and what never to mock, fixture/factory locations, cleanup requirements, flaky-area warnings, "write a failing test first" if that's the team norm
- **Skip**: generic testing philosophy

### 4. Security / compliance / data handling

- **paths**: none (if it applies everywhere) or sensitive areas, e.g. `"src/auth/**"`, `"src/payments/**"`
- **Write**: data that must never be logged or committed, where input validation and authz checks belong, secret handling (env var names, vault), parameterized-query requirement, PII rules, the why for each
- **Note in the rule** which items are additionally enforced by a hook/permission — and recommend adding one if a "never" isn't enforced yet
- **Skip**: generic OWASP lists Claude already knows

### 5. Protected / special files (migrations, generated code, vendored code, lockfiles)

- **paths**: exactly those files, e.g. `"db/migrations/**"`, `"**/*.generated.ts"`, `"vendor/**"`
- **Write**: the constraint (append-only, never edit by hand), the correct way to change it (the regenerate command, "create a new migration with `<cmd>`"), rollback/compat requirements, the why
- **Pair with** a permission deny / hook if edits must be blocked

### 6. Architecture / domain knowledge for a module

- **paths**: the module, e.g. `"src/billing/**"`
- **Write**: dependency direction and boundaries ("billing may import from core, never the reverse"), domain terms and their exact meaning, invariants, non-obvious gotchas and their history
- **Skip**: file-by-file descriptions, overviews derivable from reading the code

### 7. Repository etiquette (branches, commits, PRs, reviews)

- **paths**: none
- **Write**: branch naming pattern, commit message format, required checks before commit/PR, base branch, what not to commit
- **Note**: if this conflicts with Claude Code's built-in git instructions, mention `includeGitInstructions` / `attribution` settings to the user; if a check must always run, suggest a hook

### 8. Developer environment quirks / tooling

- **paths**: none, or the tool's config files (e.g. `"docker-compose*.yml"`, `"*.uproject"`)
- **Write**: commands Claude can't guess (build/test/run with required flags), required env vars, tool version managers in use, OS-specific pitfalls, "don't run X, it takes 40 minutes; run Y instead"

### 9. Personal preferences (user scope, `~/.claude/rules/`)

- **paths**: usually none; language-specific ones may use globs
- **Write**: your own style and workflow preferences that hold across all projects (communication language, preferred libraries, commit habits)
- **Keep** them compatible with typical project rules — when a user rule and a project rule conflict, Claude may follow either
