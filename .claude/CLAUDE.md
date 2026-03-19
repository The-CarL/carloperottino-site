# Blog — Project Context

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
| `title`       | `string`                | yes      | —       |
| `description` | `string`                | yes      | —       |
| `date`        | `coerce.date()`         | yes      | —       |
| `updatedDate` | `coerce.date()`         | no       | —       |
| `tags`        | `array(string)`         | no       | `[]`    |
| `draft`       | `boolean`               | no       | `false` |
| `heroImage`   | `string`                | no       | —       |

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

## Writing Standards

- First person, conversational but technical. No filler intros ("In this post we will...").
- **H2** for major sections, **H3** for subsections. Never H1 (the post title is rendered as H1 by the layout).
- Short paragraphs: 3-5 sentences max.
- Code blocks with language identifiers (```ts, ```bash, etc.).
- End with a concrete takeaway or next step, not a generic summary.

## SEO

- `title`: 60 characters or fewer
- `description`: 120-160 characters

## Diagrams

- **draw.io MCP** — architecture diagrams, polished style, AWS icon support
- **Excalidraw MCP** — conceptual / whiteboard diagrams, hand-drawn aesthetic
- Export as SVG, always include `alt` text on images

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
