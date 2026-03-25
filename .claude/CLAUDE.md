# Blog - Project Context

## Tech Stack

- **Framework:** Astro 5 (static site, `type: "module"`)
- **Styling:** Tailwind CSS 4
- **Deployment:** Vercel, auto-deploys from `main`
- **Source control:** GitHub, PRs merged to `main`

## Content Collections

Content is defined in `src/content/config.ts` using Astro's Content Layer API with `glob` loader.

### Blog Schema (Zod)

| Field         | Type                    | Required | Default |
|---------------|-------------------------|----------|---------|
| `title`       | `string`                | yes      | -       |
| `description` | `string`                | yes      | -       |
| `date`        | `coerce.date()`         | yes      | -       |
| `updatedDate` | `coerce.date()`         | no       | -       |
| `tags`        | `array(string)`         | no       | `[]`    |
| `draft`       | `boolean`               | no       | `false` |
| `heroImage`   | `string`                | no       | -       |

### Frontmatter Pattern (from existing posts)

```yaml
---
title: "Post Title"
description: "120-160 char description for SEO"
date: 2026-03-01
tags: ["tag-a", "tag-b"]
---
```

- `draft`, `updatedDate`, `heroImage` are omitted when not needed (schema defaults apply).

### File and URL Conventions

- Posts live in: `src/content/blog/<slug>.md`
- Loader: `glob({ pattern: '**/*.md', base: './src/content/blog' })`
- Slug = filename without `.md` extension (used as `post.id`)
- URL: `/blog/<slug>`
- Drafts: visible in `astro dev`, filtered out in production builds (`src/lib/posts.ts`)

## Blog Co-Writing Mode

When working on a `post/*` branch, operate in co-writing mode:

- **Expect rough input.** The user will speak via voice or type quick thoughts. Don't ask them to refine their prompt. Interpret the intent and draft something. They'll redirect if it's wrong.
- **Maintain momentum.** Don't stop to ask permission before each step. Draft content, then ask if changes are needed. Bias toward action.
- **Iterate in place.** Edit the post file directly. Don't show markdown in conversation unless asked. Just update the file and summarize what changed.
- **Be a co-writer, not a transcriber.** Push back on weak ideas. Suggest better framing. Propose section structures. Flag when something reads as generic or AI-sounding.
- **Track the post state.** Know which sections are drafted, which are empty, which need revision. Offer a status check when asked "where are we?"

## Research Behavior

When asked to research a topic (or when starting a new post on an unfamiliar topic):

- **Search the web** for existing articles, blog posts, and technical content on the topic.
- **Identify who else has written about it** -- names, publications, angles they took, and what gaps exist that could be filled.
- **Surface useful data** -- stats, benchmarks, recent announcements, primary sources worth linking.
- **Save a scratchpad file** at `src/content/blog/<slug>-research.md` with the compiled findings. This file is gitignored and is for reference during writing, not for publishing.
- **Summarize key findings** in the conversation so the user can decide what to use.
- **Use subagents** for parallel research when the topic is broad enough to warrant it -- e.g., one subagent for competitive scan, another for data gathering. For simple topics, single-threaded search is fine.

Research should be a natural part of conversation, not a rigid step. The user might say "who else has written about this?" at any point.

## Diagrams and Visual Artifacts

draw.io and Excalidraw MCPs are available globally.

- **draw.io MCP** -- use for polished, production-ready diagrams: architecture diagrams, system flows, AWS service diagrams. Supports AWS/GCP/Azure icon sets.
- **Excalidraw MCP** -- use for conceptual, whiteboard-style diagrams: mental models, rough flows, comparison layouts. Hand-drawn aesthetic.
- **When to use which:** If the diagram would appear in a conference talk or technical doc, use draw.io. If it's explaining a concept or showing a rough idea, use Excalidraw.
- **Export format:** Always SVG.
- **Storage:** Save diagram files to `public/blog/<slug>/` (create the directory if it doesn't exist). Reference in markdown as `/blog/<slug>/filename.svg`.
- **Alt text:** Every image must have descriptive alt text. Not "diagram" -- describe what it shows.

## Artifact and Image Handling

- **Generated artifacts** (diagrams, charts): Save to `public/blog/<slug>/` as described above.
- **Manual additions:** If the user says "I just dropped a screenshot in" or "I added an image," check `public/blog/<slug>/` for new files and reference them in the post.
- **Image format preferences:** SVG for diagrams, PNG for screenshots, WebP/JPEG for photos.
- **Markdown image syntax:** `![Descriptive alt text](/blog/<slug>/filename.svg)`
- **Create the asset directory** (`public/blog/<slug>/`) automatically when the first artifact is generated for a post. Don't wait for the user to do it.

## Writing Standards

<!-- Writing standards are preliminary. The canonical reference is the "blog-of-blogs" post.
     After that post is written, this section should be updated to match. -->

- First person. "I" not "we."
- No filler intros. Start with the point.
- **Never use em dashes (`---`) or en dashes (`--`).** Rewrite the sentence instead. Use commas, colons, or hyphens.
- No AI-sounding patterns: "Let's dive in," "Here's the thing," "It's worth noting," "Essentially," "Fundamentally." Be direct.
- No generic summaries at the end. End with a concrete takeaway, opinion, or forward-looking thought.
- **H2** for major sections, **H3** for subsections. Never H1 (the post title is rendered as H1 by the layout).
- Short paragraphs: 3-5 sentences max.
- Code blocks with language identifiers (```ts, ```bash, etc.).
- Working code examples, not pseudocode.
- Link to official docs rather than restating them.
- When referencing research or others' work, link to the source. Don't just mention it.

## SEO

- `title`: 60 characters or fewer
- `description`: 120-160 characters

## Build & Dev Commands

| Command             | What it does           |
|---------------------|------------------------|
| `npm run dev`       | Start dev server       |
| `npm run build`     | Production build       |
| `npm run preview`   | Preview production build |

## Git Conventions

- Blog branches: `post/<slug>`
- Commit prefix: `docs:`
- Example: `docs: scaffold post "my-new-post"`
