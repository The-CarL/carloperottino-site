---
title: "Farewell, AWS"
description: "Today was my last day at AWS. A short note on a long arc: BMW, EMR, SageMaker, re:Invent, and why I'm moving on."
date: 2026-04-03
tags: ["aws", "career"]
---

## A short note

Today was my last day at AWS. I'm leaving for a new role outside the company, and I wanted to mark the moment instead of letting it slide by in a LinkedIn update.

AWS was the first cloud I ever touched, and it's the platform I built my career on. I've worked in Azure and GCP since, and I've shipped real things on all three, but AWS is the one that taught me how to think about cloud in the first place. Most of the instincts I rely on every day got formed there.

## Where it started

My first exposure to AWS was back in college. I was interning at BMW, and somehow, as an undergrad, I ended up effectively managing our Hadoop cluster. We were running it for ML workloads across the group, and it was the kind of infrastructure responsibility you should probably not be handing to a sophomore, but there I was.

This was right when EMR was first coming out. I got to stand up EMR clusters and run the same kinds of workloads we were running on our own tin, and the contrast was immediate. On our cluster, everything was a wrestling match. Capacity planning, node failures, rebalancing, patching. On EMR, I could spin up a cluster, run a job, and tear it down. The elasticity of it genuinely changed how I thought about infrastructure. I didn't have the vocabulary for it at the time, but I remember thinking: this is a different category of thing. This is going to eat the world.

I don't think I ever really let go of that moment. Everywhere I went after that, I was looking for more of it.

## The arc through GE

A few years later I was at GE, and the majority of my work was ML. This was right when SageMaker was starting to get pushed hard by our AWS reps, and I don't know exactly where it was in its lifecycle, but for us it was new, and it was a revelation. Up to that point, the gap between "we have a model" and "we have a model in production" was enormous. SageMaker collapsed a lot of that gap in a way I hadn't seen before.

That experience set the pace for the rest of my career. From GE onward, I worked predominantly in AWS. Not because of loyalty, but because every time I needed to build something, the AWS service surface had the sharpest tools for the job. There's a reason they lead in market share. It's not marketing. It's that the services are, in a lot of cases, genuinely the best ones available.

So by the time I was a few years into my career, going to work for AWS had become a kind of background dream. Something I told myself I'd do eventually.

## re:Invent 2022

The thing that turned "eventually" into "now" was re:Invent in December 2022. I went as a customer, and I walked out of that week knowing I wanted to work there. Not in a vague "wouldn't that be cool" way. In a "this is the next move" way.

Part of it was the scale. I've always been drawn to systems that operate at a size most engineers never get to see up close, and AWS runs at a scale that's genuinely hard to comprehend until you're inside it. Part of it was the people I met that week, who were sharp in a way that felt different from the rest of the industry.

The thing that sealed it came later, during the interview process. I read the Amazon Leadership Principles for the first time and was surprised by how closely they tracked to how I already worked. Dive Deep. Deliver Results. Bias for Action. In other roles I'd had, those weren't behaviors that got rewarded. In some places they actively got in the way. Diving deep meant you were "in the weeds." Pushing for delivery meant you weren't "strategic enough."

Finding a culture that explicitly named those things as virtues felt like coming up for air. I wanted to operate in that environment, and I got the chance to.

## What I got to work on

Once I was inside, I was part of a group focused on infrastructure analytics, sitting at the forefront of cloud migration and cloud adoption. That was exactly the problem space I'd been circling my whole career. Helping customers make the same jump I'd made when I first stood up an EMR cluster as an intern, except now at a scale and with a set of tools I couldn't have imagined back then.

Some of the services I got to work with the most were the foundational ones: S3, EC2, the event-driven primitives. At one point I built an entire event-driven solution on top of those pieces, and I still remember the feeling of how quickly you could go from "I have an idea" to "it's running in production." That speed is the part that never gets old.

## Why I'm leaving

I took a new role where I can have higher impact, focus exclusively on AI, and work closer to the bleeding edge. That last part matters most. The space is moving fast enough that proximity to the frontier compounds. The closer you sit to where the new capabilities are landing, the more leverage you get on what to build with them.

That isn't a critique of AWS. It's a calculation about what I want to be doing with the next few years of my career, and where I think I can do my best work.

## What I'm taking with me

The bar for engineering and customer obsession that AWS sets is real, and it doesn't leave you when you walk out the door. I'm grateful to the people I worked with, the customers who trusted me with their hardest problems, and the leaders who pushed me to think bigger than I thought I could.

From an EMR cluster in a BMW lab to the inside of AWS itself. Not a bad arc. On to the next thing.
