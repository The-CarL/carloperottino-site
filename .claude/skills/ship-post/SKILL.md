---
name: ship-post
description: Finalize the current blog post -- build, commit, push, open PR, and clean up the worktree.
disable-model-invocation: true
allowed-tools: Bash, Read, Edit, Grep, Glob
---

# Ship Post -- Finalize and PR

You are finalizing a blog post. Follow these steps exactly.

## 1. Verify context

Check that we are in a git worktree on a `post/*` branch:

```bash
git rev-parse --show-toplevel
git branch --show-current
```

If the current branch does not start with `post/`, warn the user and ask whether to continue.

Extract the slug from the branch name:
```bash
SLUG=$(git branch --show-current | sed 's|^post/||')
```

Identify the post file by finding the markdown file(s) that differ from main:
```bash
git diff main --name-only -- 'src/content/blog/*.md'
```

Store the post file path as `POST_FILE`. If multiple files changed, list them and ask which one is the post being shipped.

## 2. Clean up research scratchpad

Check for and delete any research scratchpad file:
```bash
rm -f "src/content/blog/${SLUG}-research.md"
```

This file is gitignored, but remove it explicitly so it doesn't linger in the worktree.

## 3. Content check

Read `POST_FILE` and check:
- The file has content below the frontmatter closing `---` (not just empty or whitespace).
- The body is longer than 50 characters (a suspiciously short post).

If either check fails, warn the user: "This post looks empty or very short. Continue anyway?"

## 4. Image reference validation

Scan the post body for markdown image references (`![...](...)`) and check that each referenced file exists at the path relative to the project root (for paths starting with `/`, check in `public/`).

If any referenced images are missing, warn the user:
> These images are referenced in the post but don't exist:
> - `/blog/<slug>/missing-file.svg`
>
> Continue anyway, or fix the references first?

## 5. Stage and commit remaining changes

Stage the post file and any assets in the post's public directory:
```bash
git add "src/content/blog/${SLUG}.md"
if [ -d "public/blog/${SLUG}" ]; then
  git add "public/blog/${SLUG}/"
fi
git add -A
git status --porcelain
```

If there are staged changes, commit them:
```bash
git commit -m "docs: finalize post content"
```

## 6. Build

Run the build command:
```bash
npm run build
```

If the build **fails**:
- Show the error output to the user.
- Ask: "Should I try to fix the build error, or open a draft PR as-is?"
- If they want a fix, attempt it. If they want to ship, set `DRAFT_PR=true` and continue.

If the build **succeeds**, set `DRAFT_PR=false`.

## 7. Draft flag check

Read `POST_FILE` and check if `draft: true` is set in the frontmatter.

If it is, ask the user:
> `draft: true` is still set. Do you want to flip it to `false` so the post publishes when the PR merges, or leave it as a draft?

If they want to publish:
- Change `draft: true` to `draft: false` in the frontmatter (or remove the `draft` line entirely since the schema defaults to `false`).
- Stage and commit: `git add "$POST_FILE" && git commit -m "docs: mark post as published"`

## 8. Push and open PR

Extract the title and description from the post frontmatter for the PR.

```bash
BRANCH=$(git branch --show-current)
git push -u origin "$BRANCH"
```

Build the `gh pr create` command:
- `--title` = post title from frontmatter
- `--body` = PR description that includes the post's `description` field and a brief summary
- If `DRAFT_PR=true` (build failed), add `--draft`

```bash
gh pr create --title "$TITLE" --body "$(cat <<'EOF'
## New Blog Post

**Description:** <post description from frontmatter>

**Summary:** <1-2 sentence summary of what the post covers>

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Capture and store the PR URL from the output.

## 9. Clean up worktree

Store the current worktree path, then cd back to the main repo:

```bash
WORKTREE_PATH=$(git rev-parse --show-toplevel)
MAIN_REPO=$(git worktree list --porcelain | head -1 | sed 's/worktree //')
cd "$MAIN_REPO"
git worktree remove "$WORKTREE_PATH"
```

If removal fails, tell the user:
> Automatic cleanup failed. Run manually: `git worktree remove <path>`

## 10. Report

Print a summary:

```
Title:    <post title>
Branch:   <branch name>
PR:       <PR URL>
Status:   <"will publish on merge" or "draft -- won't publish yet">
```
