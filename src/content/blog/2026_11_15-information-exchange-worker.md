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

Someone has a question. Someone else already has the answer. I sit between them, carrying the question one way and the answer back. That is the exchange I mean.

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

## The capabilities need a better home

I wrote about this in [Checking In](/blog/checking-in#the-personal-workflow-gap). The gap I saw was the context layer and the work required to assemble useful automations around it. Connecting my tools wasn't enough. I still had to make the system understand how those tools, the information inside them, and my workflows fit together.

Information exchange is a very concrete example of that gap. I can ask an agent to search for an answer. But if I'm still copying a question out of an email, opening another tool, asking it to search, and carrying the result back, I'm still doing a lot of the exchange myself.

I think always-on agents, or what I call durable agents, are going to be a huge part of closing this. For this use case, I mean something that can stay involved in a workflow over time: notice an incoming question, retain the context needed to handle it, and continue the work when new information arrives. I want it available where the question comes in, rather than waiting for me to move the question somewhere else.

The surfaces aren't the whole adoption problem. But packaging this well matters. Someone shouldn't need to build their own collection of integrations and automations just to stop forwarding questions and answers. I expect this to get much better.

### The context layer comes first

Most of my context layer lives in Obsidian right now. I'm working on moving it into Pages and Spaces. There are a lot of examples of people building their own second brains and context layers, but the approaches I've seen don't yet feel consumer-grade to me.

My longer-term vision is a consolidated personal knowledge graph. It would connect the people, customers, projects, and activity across my life. If I email a customer, chat with them, and get on a call, I want an agent to understand that those interactions belong together.

I wouldn't put every email, transcript, call log, and file inside the graph. I'd use it to associate the common entities and point back to the underlying sources. The graph would help the agent find the context that matters without making me assemble it again for every question.

That's something I'm still working toward. Here's how I've approached the exchange problem with the context I already have.

### Old: the version I used locally

My previous version was a scheduled Codex task running on my machine. It scanned for new emails and Slack messages, and checked my notes for the kinds of toil I've been describing. It connected to my local context layer in Obsidian.

I gave it guidance for assessing risk. If a customer asked for information that was already public and the task assessed the response as low risk, it would post the answer directly. The point was to let it complete those straightforward exchanges instead of bringing every one back to me for manual handling.

That risk assessment was part of my workflow. It didn't make an internal answer safe to share just because the agent could find it. The public-information case was the clearest place to start.

This ran on my machine. I still had to put the pieces together and keep the workflow running there. That's part of the packaging gap I'm talking about.

![Old workflow: a scheduled Codex task scans email and Slack, uses local Obsidian context and risk guidance, and directly posts responses assessed as low risk.](/blog/information-exchange-worker/old-local-workflow-v1.svg)

### Current: dot + Spaces

My current version is a dot using my context layer in Spaces, following the same guidance. The workflow can be scheduled or proactive. The aim is to handle these exchanges across email, Slack, Teams, and the other places questions reach me.

![Current workflow: incoming questions reach a dot, which uses Spaces context and risk guidance to respond or bring a decision to me.](/blog/information-exchange-worker/current-dot-workflow-v1.svg)

### Future: a Carlo knowledge graph

The more complete Carlo knowledge graph is further out, and something I'm still building toward. It would connect shared entities across my interactions and point back to the original sources, rather than storing every piece of information in the graph.

![Future workflow: an agent consults a personal knowledge graph that connects shared entities and references original emails, chats, calls, and files.](/blog/information-exchange-worker/future-knowledge-graph-v1.svg)

## Answer it while we're still on the call

I started thinking about this while I was still at AWS. If I could route the audio from a call into a specialized system, I could have a voice agent listening alongside me. It could help with objection handling, look up relevant documentation, and do these information exchange searches while the conversation was happening.

The usual workflow starts with notes. I take notes on a customer call, and when the people I'm speaking with consent, I use automated notes. Those notes become action items. The information exchange tasks then go through the workflow I've described above.

But if the answer already exists, I want to get it during the call. I want the agent to notice a question it can answer, look it up, and bring the answer to me while we're still talking.

### The system I'm using

I've built a version of this, and I use it when customers consent. BlackHole routes the call audio into a voice agent using OpenAI speech models through the API. I also use local models for transcription.

The agent has tools it can call to find answers. One path uses tools such as web search. The other delegates work through the Codex SDK to headless Codex subagents. That gives it a way to use files and tools available locally, including Codex plugins.

![With participant consent, call audio passes through BlackHole to an OpenAI voice agent and local transcription. The agent can search the web or delegate through the Codex SDK to local Codex subagents, then surface answers and documentation to Carlo.](/blog/information-exchange-worker/call-agent-workflow-v1.svg)

It listens for questions it can help with and surfaces an answer or relevant documentation. I find it incredibly useful. Instead of writing down another question to take away and resolve, I can have the information in front of me during the conversation. Surfacing it to me also gives me a chance to judge what belongs in the customer conversation.

My longer-term vision is that agents can simply join calls with us. I want this kind of assistance to be available in the conversation without having to assemble the audio routing and tool connections myself.

## There's still a shit ton of opportunity

I've worked in big tech, or in some tech-adjacent role, for most of my career. That shapes what I see every day. I'm surrounded by people talking about agents, building with them, and trying to work out what comes next.

Dealing with the HOA brought me out of that world for a minute. I've been thinking about replacing these exchanges with AI and pushing on why we still need to pay someone to carry them out. In those conversations, I've encountered apprehension. I wouldn't even call it resistance. There's a hesitation about making the change.

I don't know exactly what's behind it. Maybe people haven't seen the tools that could do this. Maybe they don't trust them yet. Maybe they don't know where to start. I don't want to pretend I've diagnosed it from one HOA conversation.

But it made the diffusion problem feel very concrete to me. A capability can exist, and people can still be a long way from putting it into the everyday work around them.

When I hear that AI hasn't delivered on the promise the industry has talked about, I want to point to this. There's still a shit ton of opportunity sitting in exchanges as ordinary as coordinating a vendor visit. The work is happening every day. People are paying for it. And in this example, we're still discussing whether to try doing it differently.

I suspect there's a lot more of this across regional businesses, small and medium businesses, and organizations that weren't built around software. I don't have a number for it. What I have is this very ordinary interaction that made me wonder how many entire job functions still consist largely of these exchanges.

For me, it's a useful litmus test. Look at how often an existing answer still has to pass through a person before it reaches the person who needs it. Every one of those exchanges is somewhere to look for opportunity. Seeing so many of them around me makes it hard to believe we're anywhere close to exhausting it.

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

## How much of your job is this?

I'd encourage you to look at your last week of work. Open the emails, the chat threads, the meeting notes. Pick out the exchanges where somebody needed something from you and ask:

- Did I know the answer, or did I ask someone else and pass their answer back?
- Did I spend a call collecting questions that I then took to another team?
- Was I coordinating availability, checking a status, or chasing an update that already existed somewhere?
- Did I change the answer, or just make it easier to read and send it on?
- If an agent had access to the same sources and sharing rules, what would still require me?
- How much of my working week consists of those exchanges?

If this is your primary function, I think you should be incredibly concerned about depending on it. Being the person who knows whom to ask has been valuable for a long time. I wouldn't build the next stage of my career around being that person. I'd start working out what else I can contribute and how to make that a larger part of my work.

If this is a secondary or tertiary part of your job, I'd lean into replacing it proactively. Pick a recurring exchange. Give an agent the relevant context and clear limits on what it can share or do. Review what comes back, work through the failures, and use that experience to decide how much of the exchange you can hand over. Reclaim the time for work you actually want to do.

I'm applying this to myself. By my own estimate, this is a large part of my job. I want to take it apart now, while I can help decide how it changes and what I do with the time it frees up.

I hope OpenAI and other organizations build agents that take this work off our hands. I want to help build them. My next step is to work out how much of my own inbox I can hand over, and what decisions actually need to come back to me.
