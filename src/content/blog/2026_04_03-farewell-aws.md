---
title: "Farewell, AWS"
description: "Today was my last day at AWS. A short note on a long arc: BMW, EMR, SageMaker, re:Invent, and the culture I'm carrying with me."
date: 2026-04-03
tags: ["aws", "career"]
---

## A short note

Today was my last day at AWS. I'm leaving for a new role outside the company, and I wanted to mark the moment instead of letting it slide by in a LinkedIn update.

AWS was the first cloud I ever touched, and it's the platform I built my career on. I've worked in Azure and GCP since, and I've shipped real things on all three, but AWS is the one that taught me how to think about cloud in the first place. Most of the instincts I rely on every day got formed there.

## Where it started

My first exposure to AWS was back in college. I was doing a co-op in BMW's IT Innovation group in Greenville, and somehow I ended up effectively managing the group's 19-node Hadoop cluster. We were running it for ML workloads and performance benchmarking across a handful of frameworks, and it was the kind of infrastructure responsibility you probably shouldn't hand to an undergrad, but there I was.

This was right when EMR was first coming out. I got to stand up EMR clusters and run the same kinds of workloads we were running on our own tin, and the contrast was immediate. On our cluster, everything was a wrestling match. Capacity planning, node failures, rebalancing, patching. On EMR, I could spin up a cluster, run a job, and tear it down. The elasticity genuinely changed how I thought about infrastructure. I didn't have the vocabulary for it at the time, but I remember thinking: this is a different category of thing. This is going to eat the world.

I never really let go of that moment. Everywhere I went after that, I was looking for more of it.

## The arc through GE

A few years later I was at GE Digital in Cincinnati. The majority of what I did there was infrastructure analytics and infrastructure machine learning on a platform monitoring thousands of compute assets across the enterprise. At some point during that run, I built an event-driven solution as part of that work that still ranks as one of the pieces of engineering I'm proudest of. The shape of it, taking messy infrastructure signal and turning it into something actionable and self-healing, is what hooked me on event-driven architectures as a pattern for the rest of my career.

That was also the era when SageMaker showed up. The service had just been announced at re:Invent in late 2017, and our AWS reps were pushing it hard. Up to that point, the gap between "we have a model" and "we have a model running in production" was enormous. SageMaker collapsed a lot of that gap in a way I hadn't seen anywhere else. It was phenomenal, and it set the pace for how I thought about building ML systems for the rest of my career.

From GE onward, I worked predominantly in AWS. Not out of loyalty, but because every time I needed to build something, the AWS service surface had the sharpest tools for the job. There's a reason they lead in market share. The services are, in a lot of cases, genuinely the best ones available. By the time I was a few years into my career, going to work for AWS had become a kind of background dream. Something I told myself I'd do eventually.

## re:Invent 2022

The thing that turned "eventually" into "now" was re:Invent in December 2022. I went as a customer, and I walked out of that week knowing I wanted to work there. Not in a vague "wouldn't that be cool" way. In a "this is the next move" way.

Part of it was the scale. I've always been drawn to systems that operate at a size most engineers never get to see up close, and AWS runs at a scale that's genuinely hard to comprehend until you're inside it. Part of it was the people I met that week, who were sharp in a way that felt different from the rest of the industry.

The thing that sealed it came later, during the interview process. I read the Amazon Leadership Principles for the first time and realized they described how I already wanted to work. I'll come back to that.

## What I got to work on

I joined as an AI/ML Specialist Solutions Architect focused on healthcare and life sciences. Most of my days were spent designing enterprise AI/ML architectures across computer vision, agentic AI, and generative AI for some of the most regulated environments on the planet. HIPAA, GxP, GDPR. The kind of work where the constraints are as interesting as the capabilities.

I got to architect video analysis platforms spanning thousands of laboratory cameras, prototype multi-agent SaaS for scientific workflows, stand up agentic RAG for regulatory compliance, and run workshops, hackathons, and executive briefings across the US and EMEA. More than anything, I got to help customers make the same jump I'd made years earlier at BMW, except now at a scale and with a set of tools I couldn't have imagined back then.

## Why I'm leaving

I took a new role where I can have higher impact, focus exclusively on AI, and work closer to the bleeding edge. That last part matters most. The space is moving fast enough that proximity to the frontier compounds. The closer you sit to where the new capabilities are landing, the more leverage you get on what to build with them.

That isn't a critique of AWS. It's a calculation about what I want to be doing with the next few years of my career, and where I think I can do my best work.

## What I'm taking with me

Two years inside AWS gave me a lot, but three things stand out, and they're what I'm carrying with me into whatever comes next.

The first is the builder culture. Amazon is, for my money, the most robust builder culture I've seen in the industry. Everything is oriented around making it easy for people to ship things. The primitives, the internal tooling, the vocabulary, the reward structure, all of it is designed to lower the activation energy of "I have an idea" and make the distance to "it's running in production" as short as possible. That's not an accident. It's the thing they've been optimizing for since the beginning, and you feel it every day you work there.

The second is customer obsession. I'd read about customer obsession as an Amazon concept long before I joined. I assumed it was mostly branding. It isn't. It's a real, enforced, daily practice. Meetings get redirected when someone loses sight of the customer. Decisions get pushed back when they can't be traced to a customer problem. Writing starts with the customer. The amount of gravitational pull that one principle has on the culture is something I hadn't seen anywhere else.

The third is Dive Deep, and this is the one that resonated with me most personally. In most of the companies I'd worked at before, diving deep was treated as a failure mode. You were "in the weeds." You weren't being "strategic." You were missing the forest for the trees. At Amazon, diving deep is a virtue. It's one of the Leadership Principles for a reason. The expectation is that senior people should be able to drop into the details at any moment and speak to them credibly, and that asking for a deeper layer is a sign you're doing your job, not a sign you don't trust your team. Finding a culture that explicitly named that as a strength, after years of being told it wasn't one, felt like coming up for air.

I'm grateful to the people I worked with, the customers who trusted me with their hardest problems, and the leaders who pushed me to think bigger than I thought I could. From an EMR cluster in a BMW lab to the inside of AWS itself. Not a bad arc.

On to the next thing.
