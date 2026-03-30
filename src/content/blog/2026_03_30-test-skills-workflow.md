---
title: "Your CI Pipeline Is Lying to You"
description: "Green builds create false confidence. Most CI pipelines test the wrong things and miss the failures that actually matter in production."
date: 2026-03-30
tags: ["devops", "ci-cd", "testing"]
draft: true
---

## Green doesn't mean safe

Every team I've worked with has the same ritual. Push code, wait for the green checkmark, merge. The green checkmark is the security blanket of modern software development. It means nothing went wrong. It means your code is ready.

Except it doesn't mean that at all.

What it actually means is that a specific set of tests, written by someone at some point in time, passed against your change in an environment that may or may not resemble production. That's it. The green checkmark is a statement about your test suite, not about your software.

## The tests you're not running

Most CI pipelines test syntax and logic. Unit tests, maybe some integration tests. The standard pyramid. But here's what they almost never test:

- **Deployment sequencing.** Your code works, but can it deploy without downtime? Rolling updates, database migrations, feature flag coordination, none of that shows up in `npm test`.
- **Resource pressure.** Your tests run on a fresh container with no memory pressure, no noisy neighbors, no connection pool exhaustion. Production has all of those.
- **Clock and time zone behavior.** Tests run in UTC on a machine with infinite patience. Your users are in Tokyo at 2am during a daylight savings transition.
- **Dependency freshness.** Your lockfile pins versions, but the CDN your app calls doesn't have a lockfile. Neither does the OAuth provider you depend on.

I've seen teams with 95% code coverage ship bugs that cost real money because the failure mode was in the 5% that no unit test could reach.

## What a honest pipeline looks like

The honest version of CI doesn't just run tests. It asks harder questions:

```yaml
# .github/workflows/honest-ci.yml
name: Honest CI
on: [push]
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  deploy-dry-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
      - run: ./scripts/deploy-dry-run.sh

  dependency-health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --production
      - run: ./scripts/check-external-deps.sh
```

This is closer, but still incomplete. The real gap is that CI pipelines are batch validators. They answer "does this change break anything we already know about?" They can never answer "does this change break anything we haven't thought of yet?"

## The observability bridge

The missing piece is connecting your pipeline to production reality. Not just deploying and hoping, but closing the feedback loop.

Teams that do this well treat the first 15 minutes after deploy as an extension of CI. Canary metrics, error rate comparisons, latency percentile shifts. If the post-deploy numbers don't hold, the deploy rolls back automatically. No human in the loop.

This isn't new. Google's been doing it for years. But most teams I talk to treat CI and observability as completely separate concerns, managed by separate teams, with separate tools. The pipeline ends at merge. Everything after that is "ops."

That split is where bugs hide.

## The uncomfortable truth

Your CI pipeline is a confidence machine. Its job is to make you feel safe merging code. And it's very good at that job. Maybe too good.

The teams I've seen ship the most reliably aren't the ones with the most tests or the fanciest pipelines. They're the ones who treat the green checkmark with healthy skepticism. Who ask "what isn't this testing?" as often as they ask "did the tests pass?"

The green checkmark should be the start of your confidence, not the end of it.
