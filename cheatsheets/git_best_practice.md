# Git Best Practice

[📑 Table of Contents](#table-of-contents)

> Personal Git notes for learning, documenting, and improving my coding workflow.
>
> Main goal:
>
> Move from:
>
> ```bash
> git add .
> git commit -m "update"
> git push
> ```
>
> to a cleaner, more intentional workflow:
>
> ```bash
> git status
> git diff --stat
> git add <file>
> git diff --staged
> git commit -m "<type>: <description>"
> git push
> ```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# Table of Contents

- [1. Why Git Matters](#1-why-git-matters)
- [2. My Git Philosophy](#2-my-git-philosophy)
- [3. Beginner Workflow](#3-beginner-workflow)
- [4. Recommended Level 2 Workflow](#4-recommended-level-2-workflow)
- [5. Command-by-Command Explanation](#5-command-by-command-explanation)
- [6. Commit Message Format](#6-commit-message-format)
- [7. Commit Types](#7-commit-types)
- [8. Good vs Bad Commit Messages](#8-good-vs-bad-commit-messages)
- [9. One Commit = One Idea](#9-one-commit--one-idea)
- [10. Common Personal Project Examples](#10-common-personal-project-examples)
- [11. Git Add Best Practice](#11-git-add-best-practice)
- [12. Reviewing Before Commit](#12-reviewing-before-commit)
- [13. When To Use git add .](#13-when-to-use-git-add-)
- [14. When Not To Use git add .](#14-when-not-to-use-git-add-)
- [15. Git Status Patterns](#15-git-status-patterns)
- [16. Git Diff Patterns](#16-git-diff-patterns)
- [17. Safe Commit Checklist](#17-safe-commit-checklist)
- [18. Suggested Daily Workflow](#18-suggested-daily-workflow)
- [19. Learning Path](#19-learning-path)
- [20. Quick Reference](#20-quick-reference)
- [21. Notes To Future Me](#21-notes-to-future-me)

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 1. Why Git Matters

Git is not just for saving files.

Git helps me:

- Track what changed
- Recover previous versions
- Understand project history
- Document my learning
- Work more safely
- Build professional habits
- Avoid losing work
- Review my own code before saving it permanently

A good Git history is like a project diary.

If I come back after 6 months, I should understand what happened by reading the commit messages.

[⬆ Back to Table of Contents](#table-of-contents)
 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 2. My Git Philosophy

Git is not only a backup tool.

Git is a time machine.

Each commit should tell a small story.

A good commit answers:

```text
What changed?
Why did it change?
```

A bad commit only says:

```text
update
changes
latest
final
```

Future Me should not have to guess what I was doing.


 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 3. Beginner Workflow

This is the common beginner workflow:

```bash
git status
git add .
git commit -m "update"
git push
```

This works, but it is not ideal.

## Problems

```text
git add .
```

adds everything.

This might accidentally include:

- temporary files
- exported reports
- debug files
- test data
- old experiments
- files I did not mean to commit

Bad commit messages like:

```bash
git commit -m "update"
```

do not explain anything.

Example bad history:

```text
update
update again
fix
changes
latest
final
final v2
final final
working now
```

This makes the project history hard to understand.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 4. Recommended Level 2 Workflow

This is my recommended workflow while learning Git properly:

```bash
git status

git diff --stat

git add <file>

git diff --staged

git commit -m "<type>: <description>"

git push
```

Example:

```bash
git status

git diff --stat

git add abc_analysis.py

git diff --staged

git commit -m "feat: add ABC analysis report"

git push
```

This is better because I:

- check what changed
- review the size of the change
- stage files intentionally
- review staged changes before committing
- write a meaningful commit message
- push only after I understand what I committed

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 5. Command-by-Command Explanation

## git status

Use this first.

```bash
git status
```

This shows:

- changed files
- staged files
- untracked files
- current branch

Example output:

```text
On branch main

Changes not staged for commit:
  modified:   abc_analysis.py
  modified:   notes/git_best_practice.md

Untracked files:
  reports/abc_analysis.csv
```

Ask myself:

```text
What files did I change?
Do I recognise all of them?
Should all of them be committed?
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## git diff --stat

Use this to see a summary of changes.

```bash
git diff --stat
```

Example:

```text
abc_analysis.py              | 45 +++++++++++++++++++++++
notes/git_best_practice.md   | 80 +++++++++++++++++++++++++++++++++++++
2 files changed, 125 insertions(+)
```

This helps me understand the size of the change quickly.

Ask myself:

```text
Is this one logical change?
Or did I mix multiple ideas?
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## git diff

Use this to see exact unstaged changes.

```bash
git diff
```

This shows the actual line-by-line changes.

Useful before staging.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## git add <file>

Instead of adding everything:

```bash
git add .
```

prefer adding specific files:

```bash
git add abc_analysis.py
```

or:

```bash
git add notes/git_best_practice.md
```

This helps me commit intentionally.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## git diff --staged

After staging, review what will be committed:

```bash
git diff --staged
```

This is one of the most important habits.

It shows exactly what is about to go into the commit.

Ask myself:

```text
Is this clean?
Did I accidentally include debug code?
Did I accidentally include private paths?
Did I accidentally include large files?
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## git commit -m

Commit with a clear message.

```bash
git commit -m "feat: add ABC analysis report"
```

The message should be short but meaningful.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## git push

Push to GitHub.

```bash
git push
```

This uploads the commit to the remote repository.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 6. Commit Message Format

Recommended format:

```bash
git commit -m "<type>: <short description>"
```

Examples:

```bash
git commit -m "feat: add ABC analysis report"
```

```bash
git commit -m "fix: correct project root path"
```

```bash
git commit -m "docs: add Git best practice notes"
```

```bash
git commit -m "refactor: simplify pandas aggregation"
```

The format is:

```text
type: what changed
```

Keep it simple.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 7. Commit Types

## feat

Use for new functionality.

Examples:

```bash
git commit -m "feat: add ABC analysis report"
```

```bash
git commit -m "feat: add warehouse export validation"
```

```bash
git commit -m "feat: calculate SKU order frequency"
```

```bash
git commit -m "feat: add article-level inventory summary"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## fix

Use for bug fixes.

Examples:

```bash
git commit -m "fix: correct parquet input path"
```

```bash
git commit -m "fix: handle missing order id values"
```

```bash
git commit -m "fix: resolve datetime conversion error"
```

```bash
git commit -m "fix: correct project root detection"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## docs

Use for documentation.

Examples:

```bash
git commit -m "docs: add Git best practice notes"
```

```bash
git commit -m "docs: update pandas cheat sheet"
```

```bash
git commit -m "docs: add R to Python examples"
```

```bash
git commit -m "docs: document Git level 2 workflow"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## refactor

Use when cleaning code without changing behaviour.

Examples:

```bash
git commit -m "refactor: simplify ABC analysis pipeline"
```

```bash
git commit -m "refactor: organise path setup code"
```

```bash
git commit -m "refactor: move repeated logic into function"
```

```bash
git commit -m "refactor: clean dataframe formatting step"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## test

Use when adding or changing tests/checks.

Examples:

```bash
git commit -m "test: add validation checks"
```

```bash
git commit -m "test: add missing column checks"
```

```bash
git commit -m "test: verify warehouse export row counts"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## chore

Use for maintenance tasks.

Examples:

```bash
git commit -m "chore: remove old output files"
```

```bash
git commit -m "chore: update project folders"
```

```bash
git commit -m "chore: clean unused notebook cells"
```

```bash
git commit -m "chore: update gitignore"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 8. Good vs Bad Commit Messages

## Bad commit messages

```bash
git commit -m "update"
```

```bash
git commit -m "changes"
```

```bash
git commit -m "latest"
```

```bash
git commit -m "fixed"
```

```bash
git commit -m "final"
```

```bash
git commit -m "working now"
```

Problem:

These do not explain what changed.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Good commit messages

```bash
git commit -m "feat: add ABC analysis report"
```

```bash
git commit -m "fix: correct project root path"
```

```bash
git commit -m "docs: add pandas formatting notes"
```

```bash
git commit -m "refactor: simplify groupby aggregation"
```

```bash
git commit -m "chore: remove temporary CSV exports"
```

These explain the intent.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 9. One Commit = One Idea

Best practice:

```text
One commit should represent one logical change.
```

Good:

```bash
git commit -m "feat: add ABC analysis report"
```

Another commit:

```bash
git commit -m "docs: update pandas cheat sheet"
```

Another commit:

```bash
git commit -m "fix: correct project root path"
```

Bad:

```text
One commit that includes:
- ABC analysis code
- README update
- path bug fix
- shell notes
- deleted old files
```

That is too many ideas in one commit.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 10. Common Personal Project Examples

## Warehouse analytics project

If I add a new report:

```bash
git add abc_analysis.py
git commit -m "feat: add ABC analysis report"
```

If I fix the input path:

```bash
git add abc_analysis.py
git commit -m "fix: correct warehouse export input path"
```

If I update notes:

```bash
git add notes/pandas_cheatsheet.md
git commit -m "docs: update pandas groupby notes"
```

If I clean up code:

```bash
git add abc_analysis.py
git commit -m "refactor: simplify ABC aggregation pipeline"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Personal learning repo

If I add Git notes:

```bash
git add notes/git_best_practice.md
git commit -m "docs: add Git best practice notes"
```

If I add shell commands:

```bash
git add notes/shell_commands.md
git commit -m "docs: add shell command notes"
```

If I add Python examples:

```bash
git add python/pandas_examples.py
git commit -m "feat: add pandas dataframe examples"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## RStudio to Python cheat sheet

If I add column reorder notes:

```bash
git add python/r_to_python_cheatsheet.md
git commit -m "docs: add pandas column reordering examples"
```

If I fix a typo:

```bash
git add python/r_to_python_cheatsheet.md
git commit -m "docs: fix typo in pandas notes"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 11. Git Add Best Practice

## Beginner

```bash
git add .
```

This stages everything.

Fast, but risky.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Better

```bash
git add <file>
```

Example:

```bash
git add abc_analysis.py
```

This stages only one file.

 [⬆ Back to Table of Contents](#table-of-contents) 
  [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Multiple files

```bash
git add abc_analysis.py notes/git_best_practice.md
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Add a folder

```bash
git add notes/
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Add one specific Markdown file

```bash
git add notes/git_best_practice.md
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Add one specific Python file

```bash
git add scripts/abc_analysis.py
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 12. Reviewing Before Commit

Before committing, always review.

## Quick review

```bash
git status
```

## Summary review

```bash
git diff --stat
```

## Detailed review before staging

```bash
git diff
```

## Detailed review after staging

```bash
git diff --staged
```

My preferred review sequence:

```bash
git status
git diff --stat
git add <file>
git diff --staged
git commit -m "<type>: <description>"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 13. When To Use git add .

Using:

```bash
git add .
```

is okay when:

- I intentionally want to commit everything
- I already checked `git status`
- I already checked `git diff --stat`
- The changes are small
- The changes all belong to the same idea

Example:

```bash
git status
git diff --stat
git add .
git diff --staged
git commit -m "docs: update Git best practice notes"
```

This is acceptable if all changed files are documentation files related to the same note.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 14. When Not To Use git add .

Avoid:

```bash
git add .
```

when:

- I changed many unrelated files
- I edited code and documentation at the same time
- I created output files
- I have temporary files
- I am not sure what changed
- I have untracked files
- I have private data files
- I have large exported reports

Example risky situation:

```text
modified: abc_analysis.py
modified: notes/git_best_practice.md
untracked: reports/abc_analysis.csv
untracked: data/raw/private_export.csv
```

In this case, do not use:

```bash
git add .
```

Instead:

```bash
git add abc_analysis.py
```

then commit that separately.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 15. Git Status Patterns

## Clean working tree

```bash
git status
```

Output:

```text
nothing to commit, working tree clean
```

Meaning:

No uncommitted changes.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Modified file

```text
modified: abc_analysis.py
```

Meaning:

Tracked file changed.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Untracked file

```text
untracked: reports/abc_analysis.csv
```

Meaning:

Git sees a new file but is not tracking it yet.

Be careful before adding.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Staged file

```text
Changes to be committed:
  modified: abc_analysis.py
```

Meaning:

This file will be included in the next commit.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 16. Git Diff Patterns

## See unstaged changes

```bash
git diff
```

## See staged changes

```bash
git diff --staged
```

## See only file summary

```bash
git diff --stat
```

## See staged file summary

```bash
git diff --staged --stat
```

## See changed file names only

```bash
git diff --name-only
```

## See staged changed file names only

```bash
git diff --staged --name-only
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 17. Safe Commit Checklist

Before every commit, check:

```text
[ ] Did I run git status?
[ ] Did I understand what files changed?
[ ] Did I avoid committing unnecessary files?
[ ] Did I stage intentionally?
[ ] Did I review git diff --staged?
[ ] Is my commit message meaningful?
[ ] Does this commit represent one idea?
```

If yes, commit.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 18. Suggested Daily Workflow

## Start working

```bash
git status
```

Check if the working tree is clean.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## After making changes

```bash
git status
git diff --stat
```

Understand what changed.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Stage one file

```bash
git add <file>
```

Example:

```bash
git add scripts/abc_analysis.py
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Review staged changes

```bash
git diff --staged
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Commit

```bash
git commit -m "feat: add ABC analysis report"
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Push

```bash
git push
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 19. Learning Path

## Level 1

Basic workflow:

```bash
git status
git add .
git commit -m "message"
git push
```

Goal:

Understand the basic Git cycle.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Level 2

Intentional workflow:

```bash
git status
git diff --stat
git add <file>
git diff --staged
git commit -m "<type>: <description>"
git push
```

Goal:

Create cleaner commits.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Level 3

Partial staging:

```bash
git add -p
```

Goal:

Stage only part of a file.

Useful when one file contains multiple changes.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Level 4

Branching:

```bash
git checkout -b feature/abc-analysis
```

or newer syntax:

```bash
git switch -c feature/abc-analysis
```

Goal:

Work on features separately.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

## Level 5

Pull requests and code review.

Goal:

Review changes before merging into main.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 20. Quick Reference

## Check status

```bash
git status
```

## See summary of changes

```bash
git diff --stat
```

## See exact changes

```bash
git diff
```

## Stage one file

```bash
git add <file>
```

## Stage all files

```bash
git add .
```

## Review staged changes

```bash
git diff --staged
```

## Commit

```bash
git commit -m "type: description"
```

## Push

```bash
git push
```

## See commit history

```bash
git log --oneline
```

## See recent commits nicely

```bash
git log --oneline --graph --decorate
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# 21. Notes To Future Me

Do not commit just because files changed.

Commit because a small thought is complete.

A good commit is a checkpoint.

A good commit message should make sense months later.

Use Git to tell the story of the project.

Bad history:

```text
update
changes
latest
fix
final
```

Good history:

```text
feat: add ABC analysis report
fix: correct parquet input path
docs: add Git best practice notes
refactor: simplify aggregation pipeline
```

Future Me will thank Present Me for writing clear commits.

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# My Default Workflow

Use this most of the time:

```bash
git status

git diff --stat

git add <file>

git diff --staged

git commit -m "<type>: <description>"

git push
```

Example:

```bash
git status

git diff --stat

git add notes/git_best_practice.md

git diff --staged

git commit -m "docs: add Git best practice notes"

git push
```

 [⬆ Back to Table of Contents](#table-of-contents) 
 ---

# Final Reminder

The best habit is not memorising many Git commands.

The best habit is pausing before committing and asking:

```text
What changed?
Why did I change it?
Is this one idea?
```

Then write the commit message from that answer.

Example:

```text
What changed?
I added Git best practice notes.

Why?
To document my Level 2 Git workflow.

Commit:
docs: add Git best practice notes
```

```bash
git commit -m "docs: add Git best practice notes"
```
