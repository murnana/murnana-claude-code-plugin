# GitHub file size limits

Source: GitHub Docs, "About large files on GitHub" and "Repository limits"
(https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits). Re-check the numbers there when GitHub changes them.

| File size | What GitHub does on `git push` | What the hook does |
|---|---|---|
| under 50 MiB | accepts | allows |
| 50 MiB or more | warns, accepts | allows, tells Claude to warn the user |
| 100 MiB or more | blocks the push | blocks `git commit` (exit 2) |

GitHub applies these limits to files that are not stored in Git LFS. A file stored in Git LFS is replaced in the repository by a pointer of about 130 bytes, so it is not subject to them (Git LFS has its own per-file limit that depends on the plan).

## How the hook measures size

- Staged files: the size of the blob in the index (`git cat-file -s :<path>`). A file that Git LFS has converted is a pointer here, so it passes. A file that `.gitattributes` marks as LFS but that was not converted (for example `git-lfs` is not installed) is still large here, so it is blocked.
- `git commit -a` / `--all`: modified tracked files that are not staged yet are measured on disk, and paths whose `filter` attribute is `lfs` are skipped.
- Deleted files are ignored.

## Limits of this check

- It is a per-file check. It does not measure the size of the whole push or of the repository.
- It runs only for `git commit` issued through Claude Code's Bash tool.
