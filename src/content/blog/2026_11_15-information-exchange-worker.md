---
title: "The End of the Information Exchange Worker"
description: "I spend much of my working life moving information between people. I want agents to take that work, and I think we should all ask what comes after it."
date: 2026-11-15
tags: ["ai", "agents", "career"]
draft: true
---

We pay someone to help with our HOA. One of the things they do is ask a vendor when they can come on site, then bring the answer back to the board.

The vendor says December 1st. The board gets asked whether December 1st works. The answer goes back to the vendor.

In that exchange, nobody is adding judgment. Someone is carrying a message between two parties. And I keep thinking: why are we paying a person to do this?

Then I look at my own inbox.

I'm calling it information exchange work.

For probably two years, I've been watching this get harder and harder to ignore. A lot of my time at Amazon, and now at OpenAI, has involved taking information from one group of people and getting it to another. Product clarifications. Release timelines. Roadmap questions.

A customer asks me something. I go find the answer. Sometimes that's in documentation. Sometimes it's spread across internal conversations. Sometimes I ask someone on the product team. Then I put the answer together, work out what I can share, and send it back.

That can be insanely valuable to the customer. It's also high toil for me. And increasingly, I struggle to explain why Carlo, a human, needs to sit in the middle of that exchange.

I've always hated this part of the job. I'm tremendously excited about the possibility of getting rid of it.

![A person passes an unchanged message along a gold connection between a sender and a recipient.](/blog/information-exchange-worker/information-relay-v1.webp)

## I'm mostly finessing

This became more obvious when I moved from consulting into product organizations. There's a whole category of questions that comes with being close to a product team.

Can I get into this alpha? How does this system work under the hood? Can I meet with a subject matter expert? What's the roadmap? Why was it designed this way?

The product team has knowledge that isn't all publicly available. People like me become the interface to it. It can look like gatekeeping, but most of the time, I'm just finessing. Finding the right person. Finding the right conversation. Working out how to phrase an answer for this particular customer.

Even before AI, I thought it was a poor use of my time. It mattered because someone needed the answer, and finding and communicating that answer took work.

There wasn't a mechanism I trusted to take a question, scan multiple sources, and apply judgment to a response. Now I see a path to building exactly that.

## The answer already exists

These questions come through email, Slack, Teams, and on customer calls. When is this being released? What is this alpha? How specifically does this feature work under the hood?

There's a concrete answer. I might not have it, and it might not be documented publicly, but someone has it. My job in that moment is to go get it from them and bring it back. That whole exchange feels like a colossal waste of time.

The customer needs the answer. I want them to get it faster. Having me search for the person or conversation that holds it is the part I want to remove.

## I want this across every surface

Here's a very concrete thing I want: a customer emails me a roadmap question, and an agent finds the relevant internal context and responds with what that customer is allowed to know.

On a call, I want the customer's question to trigger that lookup while we're still talking. I've already built a version of this: when those kinds of questions come up, I can automatically search Slack. I want the answer there in the conversation, without having to go away, find someone, and come back later.

The surface changes. The exchange is the same.

The obvious risk is leaking sensitive information. Access to an internal Slack conversation doesn't mean permission to repeat it to a customer. Knowing a tentative date doesn't mean being authorized to make a commitment.

But deciding what can be shared is already part of the work I do manually. I want to make those rules explicit enough that an agent can handle the exchanges within them and bring me the ones that need a decision. I feel much more comfortable trying to build that today than I did before.

And that's the harder case. I also get questions where the answer is already documented. It blows my mind how often a customer asks me something they could have asked ChatGPT or Codex themselves. I'm still there, manually completing the exchange.

I want to stop doing that. I want to help build the system that lets me stop.

## The part I might actually miss

Architecture feels different to me. I enjoy taking a customer's problem, decomposing it into something specific, and asking the hard questions. There's something to work out together. We aren't just retrieving an answer someone already has.

That's the part I might mourn a bit. I see humans doing it for a little longer. I don't assume that lasts forever. I can picture a solution architecture agent on AWS that reviews a design and works through it with you. I expect agents to take on more of that work too.

But my immediate frustration is the volume of exchanges where the answer already exists and I'm the person ferrying it around. I'd estimate information exchange makes up 70 percent of my job. That's enough that I can't treat this as a marginal productivity improvement.

## What is the remaining unit of work?

The HOA example is the easiest version to spot. Information comes in, information goes out, and the person in the middle hasn't changed the decision. But I want a useful way to examine the harder cases too, including my own.

Here's the test I'm starting with. Take one exchange from your day. Did the answer already exist before the question reached you? Where did you go to get it? What happened between receiving it and sending it on?

| What did I add? | What I'd ask next |
| --- | --- |
| I passed along the message or coordinated a date. | What requires a person to relay this? |
| I summarized, translated, or reformatted it. | Can an agent produce the version the recipient needs? |
| I filtered it using account history or other information. | Can I give the agent authorized access to that context? |
| I applied judgment. | What decision did I make, and could I explain the basis for it? |
| I made a commitment or exercised authority. | Who is allowed to make that commitment, and who owns the outcome? |
| I helped someone trust the answer or agree to act. | What did my relationship with that person change? |

Calling something judgment shouldn't end the conversation. If I tailored an answer because I knew which version the customer was using, that's context. If I withheld part of an internal answer because it wasn't approved for external sharing, I should be able to explain that boundary. My next question is why an agent couldn't have that information too.

![Several inputs reach a shared decision surface, where a hand selects one gold path toward an outcome and leaves another path unused.](/blog/information-exchange-worker/judgment-and-context-v1.webp)

The question is what changed at that decision point, and what information or authority made the choice possible.

That doesn't mean every decision becomes a rule I can safely hand over today. Sometimes the sources conflict. Sometimes nobody has decided what the company is willing to promise. An agent finding a roadmap discussion hasn't settled that question. The organization still needs to decide who can commit to what.

Even the HOA exchange could turn into a different kind of work. If two vendors disagree about what needs fixing, or the board needs to choose how to spend its money, someone has a decision to make. My frustration is with paying for the relay and treating it as though that decision happened.

I want to apply that same scrutiny to myself. Where I say I'm adding judgment, I should be able to point to it.

I hope OpenAI and other organizations build agents that take this work off our hands. I want to help build them. My next step is to work out how much of my own inbox I can hand over, and what decisions actually need to come back to me.
