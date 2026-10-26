# Carlo Perottino site style guide

The personal site shares a warm, restrained, technical visual language with [Forge](https://forge.carloperottino.com). The personal site uses muted gold for its editorial and portfolio identity; Forge uses ember orange for its workshop and experiment focus. Keep the same visual restraint across both.

Read this guide before designing UI, creating editorial artwork, or writing image-generation prompts. These are defaults; a specific user brief can override them. Existing artwork is context, not an automatic style reference.

## Visual foundations

- Use Inter for headings and body text, and JetBrains Mono for small technical labels and metadata.
- Use generous space, clear hierarchy, fine borders, modest corner rounding, and outlined tags.
- Keep grain, background glow, and motion subtle. Texture supports the composition without becoming its subject.
- Let typography and the author's ideas lead. Add an illustration when it helps communicate the subject; posts do not require a cover image.
- Treat [src/styles/global.css](src/styles/global.css) as the source of truth for implemented theme tokens.

| Role | Dark theme | Light theme |
|---|---|---|
| Background | Charcoal `#0a0a0a` | Warm paper `#faf8f5` |
| Secondary surface | `#111111` | `#f0ece6` |
| Main text | Warm cream `#f0ece6` | Warm black `#1c1917` |
| Primary accent | Muted gold `#c9a86c` | Ochre gold `#9a7530` |
| Accent highlight | `#d4b87e` | `#b08a3e` |

## Image-generation styling

### Subject and composition

- Start with the article's specific idea or point of view. Choose one clear visual metaphor that adds meaning to the writing.
- Build around one dominant subject or relationship, a few supporting forms, and generous negative space. The idea must survive at a reduced size.
- Favor clean geometry, precise linework, and simple matte objects. Restrained dimensional editorial illustration is welcome when its forms remain simple.
- Keep essential content within the central 80% of the image. Leave the article title, metadata, borders, and rounded corners to the surrounding UI.

### Color, material, and light

- Build most of the image from charcoal, warm ivory, and warm grays. Use muted gold sparingly to show the meaningful connection or focal detail.
- Use soft, controlled lighting, readable silhouettes, and matte or lightly translucent materials. A small glow can indicate a signal or relationship.
- Use fine grain only when it remains quiet at display size. Check that the image sits comfortably in both site themes; one image can serve both.
- For an article about a Forge project, reuse the core metaphor and composition. If making a separate Forge cover, adapt the accent to its ember palette.

### Avoid by default

- Smiling robot mascots, padlock parades, floating brains, generic circuit wallpaper, or other stock AI/security symbols used as the whole concept.
- Cinematic sci-fi sets, weathered industrial metal, chrome-heavy rendering, dramatic spotlights, heavy bloom, neon cyberpunk palettes, or visual clutter.
- Tiny explanatory details, dense grids, embedded titles, fake interface text, logos, watermarks, and baked-in card frames.

### Choose the right medium

Use image generation for conceptual covers and editorial illustrations. Use editable SVG for exact architecture, labeled flows, icons, and diagrams; use screenshots to show actual product behavior. Diagrams and charts may use additional colors when needed to communicate meaning. Keep their labels and structure readable.

The existing diagram workflow still applies: draw.io for polished architecture and system flows, Excalidraw for conceptual sketches, and SVG exports. See the diagram and artifact instructions in [AGENTS.md](AGENTS.md) and [.claude/CLAUDE.md](.claude/CLAUDE.md).

## Formats and asset handling

- Use landscape **16:9** as the default for editorial cover illustrations. The current [PostLayout.astro](src/layouts/PostLayout.astro) displays a hero at its natural aspect ratio, so a different ratio may suit the content.
- Save selected blog raster assets under `public/blog/<slug>/`, normally as optimized WebP. Keep editable diagrams as SVG and screenshots as PNG.
- Use descriptive, versioned filenames when iterating. Set `heroImage` in the post frontmatter only when the image is being used as the hero; use root-relative Markdown image URLs for inline artwork.
- Provide descriptive alt text for inline images. The current hero component uses the post title as alt text; ensure any essential meaning in the illustration is also available in the surrounding prose.

## Reusable generation prompt

Replace the bracketed fields for each request. Describe a fresh scene; do not carry over objects from an unrelated cover.

```text
Use case: stylized-concept.
Asset: standalone editorial illustration for Carlo Perottino's site,
landscape 16:9.
Concept: [specific article idea and one clear visual metaphor].
Subject: [one dominant subject or relationship, with minimal supporting forms].
Style: warm, restrained, technical editorial illustration; clean geometry,
precise forms, matte surfaces, subtle depth and soft controlled lighting.
Palette: charcoal #0a0a0a, warm ivory #f0ece6, warm grays,
with sparse muted-gold #c9a86c accents on meaningful details.
Composition: generous negative space, a strong silhouette readable at reduced
size, essential content inside the central 80%, clean edges.
No text, logos, watermark, border, or card mockup. Avoid robot mascots,
padlock parades, cinematic sci-fi, weathered metal, chrome, and heavy bloom.
```

Example concept for agent authorization: a simple matte relay carries a translucent human credential toward two tool ports. A thin gold connection reaches the permitted port; the other path ends at a quiet boundary. Keep the forms large and the credential abstract, without tiny text or elaborate machinery.

## Review before use

Check the image at article width and at roughly 320 px wide, beside the heading and prose, and in light and dark mode. Confirm that the metaphor is legible, the accent remains restrained, and the image complements the typography. Simplify if it competes with the page. Record the chosen prompt with the image handoff so later illustrations can repeat the treatment.
