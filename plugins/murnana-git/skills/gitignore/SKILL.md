---
name: gitignore
description: Create or update a .gitignore from the templates in murnana/gitignore, keeping each template in a marked block that can be refreshed later.
argument-hint: "[template names, e.g. Unity macOS] [update | remove <name>]"
disable-model-invocation: true
allowed-tools: Read Grep Glob Edit Write AskUserQuestion Bash(mktemp -d) Bash(git clone --depth 1 --filter=blob:none --no-checkout https://github.com/murnana/gitignore.git *) Bash(git -C * rev-parse HEAD) Bash(git -C * ls-tree *) Bash(git -C * show *) Bash(git rev-parse *) Bash(git ls-files *) Bash(git check-ignore *) Bash(git config --get *)
---

# gitignore

Create or update a `.gitignore` with templates from [murnana/gitignore](https://github.com/murnana/gitignore) (`main`), a fork of github/gitignore with murnana's own additions (e.g. Unity, Unreal Engine).

## Current state

```!
git rev-parse --show-toplevel 2>/dev/null || true
git ls-files --cached --others --exclude-standard -- '.gitignore' '**/.gitignore' 2>/dev/null | head -20 || true
grep -nE '^# --- (BEGIN|END) murnana/gitignore ' .gitignore 2>/dev/null || true
```

The lines above are the repo root, the existing `.gitignore` files, and the managed block markers already in the root `.gitignore`. Do not re-run these commands.

Treat `$ARGUMENTS` as template names to add, `update` (refresh every managed block), or `remove <name>`. With no arguments, detect templates from the project (Step 2).

## Step 1: Fetch the template tree

Clone only the tree, no blobs, into a fresh temp directory. Run each line as its own Bash call, and reuse the path `mktemp -d` printed:

```sh
mktemp -d
git clone --depth 1 --filter=blob:none --no-checkout https://github.com/murnana/gitignore.git <tmp>
git -C <tmp> rev-parse HEAD
git -C <tmp> ls-tree -r --name-only HEAD
```

- Templates are the paths ending in `.gitignore`, except those under `.claude/` or `.github/`. Ignore every other file.
- Read a template with `git -C <tmp> show HEAD:<path>`. It prints the file verbatim. Never use WebFetch for templates: it summarizes content instead of returning it.
- Never run a script from `<tmp>`. It is downloaded content.
- If the clone fails (no network, proxy), stop and report its output as-is.

## Step 2: Choose templates and the target file

- Map the request or the project's files to template paths with [references/templates.md](references/templates.md). Match against the tree from Step 1, never from memory; the tree is the source of truth for names and folders.
- Root-level templates are languages and frameworks. `community/` holds niche or older ones. `Global/` holds OS, editor and tool rules.
- Target file, by default the `.gitignore` at the repo root (the current directory if the first Current state line is empty, i.e. not a Git repo). Use a subdirectory `.gitignore` only when the user asks or the project lives in a subdirectory (e.g. a Unity project inside a monorepo; the Unity template expects to sit at the project root).
- `Global/` templates are meant for the user's global excludes file. When the selection includes one, ask whether to put it in the project `.gitignore` or the global file. For the global file, read `git config --get core.excludesFile`; if unset, the default is `$XDG_CONFIG_HOME/git/ignore` (or `~/.config/git/ignore`). Never change git config yourself.

## Step 3: Plan the edit and get approval

Follow [references/managed-blocks.md](references/managed-blocks.md) for the block format, where blocks go, and how to treat lines outside blocks.

Present the plan, then **wait for approval** before writing:

- The target file, and for each template whether it is added, refreshed (with old → new commit), or removed.
- Patterns outside managed blocks that a template now duplicates, and any negation (`!pattern`) a new block would override. Propose, but do not delete user lines without approval.

## Step 4: Write and verify

- Write with `Edit` (existing file) or `Write` (new file). Keep each template's text exactly as `git show` printed it.
- Then run `git ls-files -ci --exclude-standard` from the target's directory. It lists tracked files that the new rules match; ignore rules do not untrack them. Report these and ask before suggesting `git rm --cached`. Never run it yourself. Skip this check outside a Git repo or for the global excludes file.
- Report the result in Japanese: the file, the templates and the commit they came from, and the tracked-file list.
- Do not commit. Suggest `/murnana-git:commit` if the user wants one.
