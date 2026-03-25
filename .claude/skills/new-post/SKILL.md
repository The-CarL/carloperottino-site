---
name: new-post
description: Create a worktree and scaffold a new blog post, ready for co-writing.
disable-model-invocation: true
argument-hint: <post-slug>
allowed-tools: Bash, Read, Write, Grep, Glob
---

# New Post — Workspace Setup

You are setting up a new blog post workspace. Follow these steps exactly.

## 1. Parse the slug

The slug is provided in `$ARGUMENTS`.

- If `$ARGUMENTS` is empty, ask the user for a slug and stop.
- Sanitize: lowercase, replace spaces and underscores with hyphens, strip anything that isn't `[a-z0-9-]`.
- Store the sanitized slug as `SLUG`.

## 2. Preflight checks

Run these checks. If any fail, report the issue and stop.

```
git rev-parse --is-inside-work-tree   # must be a git repo
which gh                               # gh CLI must be installed
git status --porcelain                 # working tree must be clean (empty output)
```

If the working tree is dirty, tell the user to commit or stash changes first.

## 3. Fetch and checkout main

```bash
git fetch origin main && git checkout main && git pull origin main
```

## 4. Create a worktree

Set `BRANCH=post/$SLUG`.

Check if the branch already exists locally or remotely:
```bash
git branch --list "$BRANCH"
git ls-remote --heads origin "$BRANCH"
```

If the branch exists, append a timestamp: `BRANCH=post/${SLUG}-$(date +%s)`. Inform the user of the adjusted branch name.

Create the worktree in a sibling directory:
```bash
WORKTREE_DIR="../carloperottino-site--post-${SLUG}"
git worktree add -b "$BRANCH" "$WORKTREE_DIR" main
```

Then cd into the worktree directory.

## 5. Scaffold the blog post

Read an existing post from `src/content/blog/` to confirm the frontmatter pattern.

Create the file `src/content/blog/${SLUG}.md` with this content (adjust if the existing post pattern differs):

```markdown
---
title: ""
description: ""
date: YYYY-MM-DD
tags: []
draft: true
---

```

- Set `date` to today's date.
- Leave `title`, `description` empty — the user will fill these in during co-writing.
- Set `draft: true`.
- Leave the body empty (just a blank line after the closing `---`).

## 6. Create the asset directory

```bash
mkdir -p "public/blog/${SLUG}"
```

This directory will hold diagrams, screenshots, and other artifacts for the post.

## 7. Commit the scaffold

```bash
git add "src/content/blog/${SLUG}.md" "public/blog/${SLUG}/"
git commit -m "docs: scaffold post \"${SLUG}\""
```

## 8. Report and stop

Print a summary:

```
Branch:    post/<slug>
Worktree:  <absolute path to worktree>
Post file: src/content/blog/<slug>.md
Assets:    public/blog/<slug>/
```

Then tell the user:

> The workspace is ready. Describe what you want to write about and we'll build the post together.

**Do NOT start writing content.** Wait for the user to describe their topic.
