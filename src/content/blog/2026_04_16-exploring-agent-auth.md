---
title: ""
description: ""
date: 2026-04-16
tags: ["ai", "security", "agents", "authorization", "mcp", "oauth", "keycloak"]
draft: true
---

## Why a follow-up on authorization

<!--
Opening. Peer feedback after the eight dimensions post. Authorization was the dimension
people wanted to go deeper on. Authentication gets the attention, but authorization is
where the patterns multiply. Once you know who someone is, the question of what they're
allowed to do has way more possible answers than most teams realize.

Link back to the original post: /blog/agent-security
-->

## The forge

<!--
Introduce the exploring-agent-auth repo as a companion artifact.
- 8 runnable Jupyter notebooks, same agent, same prompts, same three users
- Only the auth code changes between patterns (two files: mcp_auth.py, service_auth.py)
- Keycloak + OPA + FastAPI, all local via Docker Compose
- If you want to get your hands dirty, head to the repo
- Link: https://github.com/The-CarL/exploring-agent-auth
-->

## The architecture

<!--
Brief overview of the system: Agent <-> MCP Server <-> Backend Service
The MCP server is infrastructure, not an authz decision point.
Three users: alice (employee), bob (manager), dave (admin). Same query, different results.
Diagram placeholder below.
-->

![Architecture overview: Agent communicates with Expense and Document MCP servers, which proxy to FastAPI backend services](/blog/exploring-agent-auth/architecture.svg)

## The three tiers

<!--
Frame the 8 patterns into three tiers before diving in:
1. Agent-side authz (1-4): service trusts the MCP server, blind to user identity
2. Service-verified identity (5-6): service validates JWT independently via JWKS
3. Fine-grained + consent (7-8): per-resource authz, then user out of credential chain

Each tier fixes a class of weakness from the one before it.
-->

## Pattern 1: Service credential

<!--
- MCP sends: static API key
- Service: validates key, no user identity
- Problem exposed: alice, bob, dave all see the same data
- Weakness: no user context reaches the service
-->

![Pattern 1 diagram: MCP server sends shared API key to backend service, no user identity forwarded](/blog/exploring-agent-auth/pattern-1.svg)

## Pattern 2: Identity parameter

<!--
- MCP sends: API key + X-User-Id header
- Service: trusts the header, filters by username
- Fix over P1: service now has user context, can filter data per-user
- Weakness: no crypto proof the header is legitimate, forgeable if MCP compromised
-->

![Pattern 2 diagram: MCP server sends API key plus X-User-Id header to backend service](/blog/exploring-agent-auth/pattern-2.svg)

## Pattern 3: Inline claim authorization (agent-side)

<!--
- MCP reads JWT claims, narrows query parameters before sending request
- Service only sees API key, has no idea narrowing occurred
- Fix over P2: uses JWT claims instead of trusting a raw header
- Weakness: authz scattered across agent code, service can't verify narrowing happened
-->

![Pattern 3 diagram: MCP server reads JWT claims and narrows query parameters, service only sees API key](/blog/exploring-agent-auth/pattern-3.svg)

## Pattern 4: External authorization, agent-side (OPA)

<!--
- MCP checks OPA before each tool call: "is this user allowed to invoke this tool?"
- OPA denies = tool call never leaves the MCP server
- Service still only sees API key
- Fix over P3: authz externalized to OPA, not scattered in agent code
- Weakness: service still blind, if MCP compromised OPA check skippable
- This is the ceiling for agent-side authz. Everything past here requires service-side verification.
-->

![Pattern 4 diagram: MCP server checks OPA policy before forwarding request with API key to backend service](/blog/exploring-agent-auth/pattern-4.svg)

## Pattern 5: JWT passthrough

<!--
- MCP sends: Bearer JWT (the user's original token), no API key
- Service: validates JWT signature via Keycloak JWKS, extracts claims
- Fix over P4: service independently verifies identity, no shared secret needed
- Weakness: token audience is broad (covers multiple services), confused deputy risk
- This is the inflection point: service-verified identity
-->

![Pattern 5 diagram: MCP server passes user JWT to backend service, service validates via JWKS](/blog/exploring-agent-auth/pattern-5.svg)

## Pattern 6: Token exchange (RFC 8693)

<!--
- MCP exchanges user's JWT for a narrowed token scoped to the target service
- Service sees: scoped aud (one service only) + azp (identifies the agent)
- Fix over P5: audience narrowed, blast radius limited
- Keycloak Standard Token Exchange v2 (GA in 26.2+)
- Note on act claim vs azp
- Weakness: MCP more complex, agent still holds user's original JWT
-->

![Pattern 6 diagram: MCP server exchanges user JWT for scoped token via Keycloak, sends narrowed token to backend service](/blog/exploring-agent-auth/pattern-6.svg)

## Pattern 7: Tool-side external authorization (ReBAC)

<!--
- MCP sends Bearer JWT, service validates + checks OPA for per-resource decisions
- OPA ReBAC: "can bob approve alice's expense?" based on reporting relationships
- Fix over P6: per-resource authz, not just role-based
- tool_side.rego: relationship-based rules (manages, department peers)
- Weakness: requires OPA integration at the service, static relationship data
-->

![Pattern 7 diagram: backend service validates JWT and checks OPA for per-resource authorization decisions](/blog/exploring-agent-auth/pattern-7.svg)

## Pattern 8: Three-legged OAuth (consent)

<!--
- User explicitly consents via browser, agent receives token out-of-band
- Agent is removed from the credential chain entirely
- Fix over P7: user controls what the agent can access, not the other way around
- The end state: agent never touches raw credentials
- Note: demo uses notebook callback, production would be full PKCE + auth code flow
-->

![Pattern 8 diagram: user consents via browser, Keycloak issues token directly, agent removed from credential chain](/blog/exploring-agent-auth/pattern-8.svg)

## What's next

<!--
Closing. Where this fits in the broader agent security taxonomy.
What's still out of scope (capability tokens, mTLS, gateway identity injection, scopes).
Each of those is its own teaching artifact.
-->
