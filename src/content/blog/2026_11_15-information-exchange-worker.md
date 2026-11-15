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

For probably two years, I've been watching this get harder and harder to ignore. A lot of my time at Amazon, and now at OpenAI, has involved taking information from one group of people and getting it to another. Product feedback. Product clarifications. Release timelines. Roadmap questions.

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

## I want an agent answering those emails

Here's a very concrete thing I want: a customer emails me a roadmap question, and an agent finds the relevant internal context and responds with what that customer is allowed to know.

The obvious risk is leaking sensitive information. Access to an internal Slack conversation doesn't mean permission to repeat it to a customer. Knowing a tentative date doesn't mean being authorized to make a commitment.

But deciding what can be shared is already part of the work I do manually. I want to make those rules explicit enough that an agent can handle the exchanges within them and bring me the ones that need a decision. I feel much more comfortable trying to build that today than I did before.

And that's the harder case. I also get questions where the answer is already documented. It blows my mind how often a customer asks me something they could have asked ChatGPT or Codex themselves. I'm still there, manually completing the exchange.

I want to stop doing that. I want to help build the system that lets me stop.

## Feedback has the same problem

Feature requests are another example. A customer tells me what they want. I ask follow-up questions, try to understand the use case, refine the request, and pass it along.

I already find AI very good at that process: iterating on feedback, asking follow-up questions, and helping someone work out what they actually want. I don't see a good reason that collecting and clarifying every request needs to pass through me.

I might have account context. I might know the customer's history, what they've tried, or why this request matters to them. That's useful. But I don't think it's reasonable to assume that context will always belong exclusively to a person. An agent can be given account context too.

The question I keep asking myself is: what am I actually adding in this particular exchange?

## I've been asking this about architects too

At AWS, I used to joke with peers that we should build a solution architecture agent.

A solutions architect helps qualify a customer use case, understand the requirements, and work toward a design that can eventually be taken into production. In my experience, AI is already a better architect than many of the architects I've worked with. It can ask follow-up questions, explore designs, and reason through tradeoffs at a level I find extremely useful.

So why wouldn't I want a solution architecture agent? I do. I want it to exist.

I feel similarly about a significant part of my work as an Applied AI Architect at OpenAI. I'd estimate information exchange makes up 70 percent of my job. That's enough that I can't treat this as a marginal productivity improvement.

My blunt view is that a big reason these customer-facing roles persist is that they're sales-centric. My experience is that customers still want to buy from and engage with other people. I think that preference explains a lot about why the human is there, even as the technical exchange becomes something an agent can increasingly handle.

I want to be honest with myself about which part of the job depends on that relationship, and which part I'm still doing because the customer happened to send the email to me.

## What is the remaining unit of work?

The HOA example is the easiest version to spot. Information comes in, information goes out, and the person in the middle hasn't changed the decision. But I want a useful way to examine the harder cases too, including my own.

Here's the test I'm starting with. Take one exchange from your day and ask what happened between receiving it and sending it on.

| What did I add? | What I'd ask next |
| --- | --- |
| I passed along the message or coordinated a date. | What requires a person to relay this? |
| I summarized, translated, or reformatted it. | Can an agent produce the version the recipient needs? |
| I filtered it using account history or other information. | Can I give the agent authorized access to that context? |
| I applied judgment. | What decision did I make, and could I explain the basis for it? |
| I made a commitment or exercised authority. | Who is allowed to make that commitment, and who owns the outcome? |
| I helped someone trust the answer or agree to act. | What did my relationship with that person change? |

Calling something judgment shouldn't end the conversation. If I filtered a feature request because I knew the customer had already tried another approach, that's context. If I chose between two designs because one better fits a constraint, I should be able to say what that constraint was. My next question is why an agent couldn't have that information too.

![Several inputs reach a shared decision surface, where a hand selects one gold path toward an outcome and leaves another path unused.](/blog/information-exchange-worker/judgment-and-context-v1.webp)

The question is what changed at that decision point, and what information or authority made the choice possible.

That doesn't mean every decision becomes a rule I can safely hand over today. Sometimes the sources conflict. Sometimes nobody has decided what the company is willing to promise. An agent finding a roadmap discussion hasn't settled that question. The organization still needs to decide who can commit to what.

Even the HOA exchange could turn into a different kind of work. If two vendors disagree about what needs fixing, or the board needs to choose how to spend its money, someone has a decision to make. My frustration is with paying for the relay and treating it as though that decision happened.

I want to apply that same scrutiny to myself. Where I say I'm adding judgment, I should be able to point to it.

I hope OpenAI and other organizations build agents that take this work off our hands. I want to help build them. My next step is to work out how much of my own inbox I can hand over, and what decisions actually need to come back to me.
