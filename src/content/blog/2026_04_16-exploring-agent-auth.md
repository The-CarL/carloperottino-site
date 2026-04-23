---
title: "Climbing the agent authorization ladder"
description: "Authentication gets the attention. Authorization is where the patterns multiply. Eight of them, runnable, from shared API key to OAuth consent."
date: 2026-04-16
tags: ["ai", "security", "agents", "authorization", "identity", "mcp", "oauth"]
---

## Why a follow-up on authorization

A couple of months ago I wrote a post on [agent security](/blog/agent-security). I laid out eight dimensions. Authorization was one of them, and I did not do it justice.

That's not a small miss. You can get seven of those eight dimensions right and still have a compromised system if the authorization piece is weak. Once you get down to specific user and tool authorization, the rest of the work you did stops mattering if this part is broken.

Honestly, I'm excited to get back into it. It's the thing I hear from customers constantly. They want someone to paint a clear picture. They want a few architectural patterns they can point at and say "these are the options." Admittedly, I wanted the same thing for myself. I wanted to be sure I understood each pattern well enough to explain it cleanly, not just wave at the concept.

This post is also shaped by feedback I got directly on the first one. Specific pushback, deeper questions, people pointing at exactly where the eight-dimensions framing skipped past the hardest bit. That's what I'm going back through here.


## The forge

Forge is a space I've been wanting for a while. Somewhere to build and ship quickly without it being a blog, an experience, or a résumé embodied in a website. Just a space for random things. Some might turn into product. Some I just want to goof off with. I didn't have a spot for either.

The vision is multi-dimensional. Sometimes a Forge entry is a pointer to something else with a short explanation. Sometimes it's a dedicated space that hosts the idea itself. Sometimes it's a pointer out to another application or platform I'm building on. The common thread is that Forge is a catalog.

This post's companion lives there: [exploring-agent-auth](https://forge.carloperottino.com/projects/exploring-agent-auth).

What I wanted to build was a seamless way to represent eight different agent-to-tool authorization patterns. You'd think that's pretty simple. It turns out to be a huge pain in the rear the moment you try to avoid massive code duplication.

I knew I needed an identity service, an agent, and backend services. I wanted MCP tools in the mix. The example backends (document service, expense service, the usernames) I had OpenAI models generate.

The hard question was architectural. Do you build eight full copies of the infrastructure, one per pattern? Do you build one instance that's aware of every authorization mechanism and switches between them? Or something in between?

Eight copies felt like poor craftsmanship. The single-instance approach doesn't match reality either. How many enterprises do you know where the architecture is "accept any authorization pattern"? None. You have an enterprise architect who picks the path, and every service adheres to it.

So I landed on a plug-in design. One construct for MCP authorization. One construct for backend-service authorization. Inside each, configurable plug-ins. Each pattern is a different combination.

Each section that follows points to the specific plug-in design for that pattern. I think it reduces duplication while keeping the patterns distinct enough that you can actually see what changes between them. It makes the repo somewhat elegant, which I'm happy about. And I'm excited to build more in Forge.


## The architecture

A core tenet for this project was that everything runs locally. No external identity provider, no hosted policy service. Clone the repo, run Docker Compose, and the whole stack is on your laptop. That makes it transparent. You can poke at every piece.

I'd never run local identity management before. Keycloak surfaced to the top of my search and I shrugged and said, sure, Keycloak. For policy I've used OPA, Oso, and Cedar in the past. I'm most familiar with Cedar, but Cedar feels more AWS-specific (I believe it's built and maintained by AWS). I wanted open source, so OPA.

One note on why there's an MCP server in the architecture at all. You can attach tools to an agent directly, in-process, and skip the MCP server entirely. I was very intentional about not doing that. In my experience, what I'm increasingly seeing is centralized, team-managed, federated, or governed MCP servers: developed and published once, consumed by many teams. The "MCP server running over stdio in the same container as the agent" pattern is not invalid. It shows up mostly on end-user development surfaces: Claude Code running locally, Claude Desktop with a few local MCP servers attached, that kind of thing. For production agent workloads, dedicated MCP servers are the shape I keep seeing.

Three users, with different permissions: alice (employee), bob (manager), and dave (admin). Each one runs through the patterns and you see the authorization outcomes, the allows and the denies, per user and per pattern.

The agent framework is [OpenAI Agents SDK](https://github.com/openai/openai-agents-python). I'm always trying new agent frameworks. I've used a lot: Strands a bunch given my AWS background, LangChain and LangGraph, a bit of CrewAI, a bit of Google's ADK, and a little OpenAI Agents SDK but not as much as I wanted. This felt like a good excuse to jump in.

The model is GPT-5 nano. I wasn't building an end-to-end agentic workflow here. Each pattern just shows the interaction, not a multi-step task, so I picked the smallest, cheapest model I could. Literally fractions of a cent per run. No serious model evaluation. I didn't care about the intelligence of the task because I'm not a big believer in models trying to discern authorization in the first place. That's not the job I want the model doing. This post is about making agent-to-tool authorization very explicit and very scalable, not about teaching a model to reason its way there.

Every pattern has its own notebook. Run them yourself.

![Architecture overview: Agent communicates with Expense and Document MCP servers, which proxy to FastAPI backend services](/blog/exploring-agent-auth/architecture.svg)

## Authentication vs authorization

This might feel trivial, but it's worth being explicit. Authentication and authorization get used interchangeably in conversation, and they are not the same thing. The patterns in this post are about authorization, and a big chunk of the confusion people have about this topic comes from those two words blurring.

**Authentication** answers: who is this? A proof of identity. A password, a valid JWT signed by an issuer you trust, a successful WebAuthn challenge. After authentication, the system can say "this is alice."

**Authorization** answers: what is alice allowed to do? Roles, claims, relationships, scopes, per-resource rules. After authorization, the system can say "alice can read her own expenses but cannot approve anyone else's."

Every pattern in this post assumes authentication has already happened. The user is who they say they are. The questions the patterns differ on are how authorization gets decided, where it gets decided, and who is on the hook. The first pattern we walk through, for the record, does no user-level authorization at all. That's a choice some systems still make, and it's worth understanding why.

## The three tiers

I'm not going to dwell here, but this framing matters for the rest of the post. The eight patterns group into three tiers, and each tier is really about two questions: who is responsible for authorization, and what level of authorization are you actually doing.

Before I name them, I want to talk about the customer conversation that made me want to write this. The example that surfaces every single time is some variation of "I've got an agent, I've got an associated database, and the database does not have a robust authorization layer on its own. I want to expose it to the agent as an MCP server. How do I do authorization here?"

There are three enterprise archetypes that show up.

The first is easy. Agent plus an existing MCP server hosted by a SaaS product: Databricks, Jira, whatever. Jira's MCP server already talks to Jira's backend and honors whatever authentication and authorization was configured there. I use the GitHub MCP regularly and it's the same story. The vendor owns the path and you inherit it.

The second is close to easy. Agent plus an internally-developed MCP server that already handles authentication and authorization, maybe using one of the patterns we're about to walk through, maybe using something enterprise-specific. Someone already did the work and you're plugging into it.

The third is the hard one, and it's the one that motivated this post. It came up in a customer conversation right before I left Amazon. Development teams with elevated credentials against production databases that don't enforce aggressive authorization on their own. The team wants to expose a backend data service for their agent to use. Now what?

Let's not pretend this is rare. It's a huge no-no, and it still happens all across the ecosystem, especially with less mature customers. It's funny to watch CISOs and architects wrap their brains around this one, because the uncomfortable answer is that someone has to be on the hook for the authorization of the workflow. If the team with elevated credentials wants to expose that service, that team is on the hook. They either build an authorization layer, lean on an existing enterprise one, or encode the rules in claims and scopes their identity provider already issues. Pick a path, but someone has to own it.

The most common failure mode I see isn't picking the wrong pattern. It's assuming this problem is somebody else's job. It isn't. My goal with the tiers is to make that concrete: it is somebody's job, and there are real options for what that job looks like. Not every system and tool needs the same configuration.

With that framing, here are the tiers.

**Tier 1: agent-side authorization** (patterns 1-4). Responsibility sits on the agent and MCP side. The backend service trusts whoever called it. Authorization happens before the request arrives, if at all.

**Tier 2: service-verified identity** (patterns 5-6). The service stops trusting the caller and independently verifies the user's identity via JWKS. The service now knows *who*, but the question of *what they're allowed to do* is still coarse.

**Tier 3: fine-grained plus consent** (patterns 7-8). The service makes per-resource authorization decisions and, in the last pattern, the user explicitly consents, which pulls the agent out of the credential chain entirely.

Each tier fixes a weakness from the one before it. The walk-through starts next, weakest to strongest.


## Pattern 1: Service credential

![Pattern 1 diagram: MCP server sends shared API key to backend service, no user identity forwarded](/blog/exploring-agent-auth/pattern-1.svg)

<details>
<summary>Code and links</summary>

**Repo:** [`patterns/p01_service_credential`](https://github.com/The-CarL/exploring-agent-auth/tree/main/patterns/p01_service_credential) · [notebook](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p01_service_credential/notebook.ipynb) · [`mcp_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p01_service_credential/mcp_auth.py) · [`service_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p01_service_credential/service_auth.py)

**`mcp_auth.py`** (MCP side):

```python
class ServiceCredentialHandler(AuthHandler):
    async def prepare_request(self, user_context, headers):
        headers["X-API-Key"] = SHARED_SERVICE_API_KEY
        return headers
```

**`service_auth.py`** (service side):

```python
EXPECTED_API_KEY = "dev-shared-api-key"

async def get_expense_identity(request: Request) -> Identity:
    api_key = request.headers.get("x-api-key")
    if api_key == EXPECTED_API_KEY:
        return Identity(
            method="api_key",
            detail="shared service credential, no user identity",
        )
    return Identity(method="none", detail="no auth provided")

# Document service uses the same auth
get_document_identity = get_expense_identity
```

</details>

The simplest version of all of this, and the baseline every other pattern will react to.

The MCP server holds a pre-shared service credential: a static API key. It attaches that key to every request it makes to the backend service. The service validates the key and, if it matches, returns data.

No user identity ever reaches the service. Run the notebook with alice, bob, and dave and you get the same answer every time. All three see the same data, because there is no user-level authorization happening anywhere. The only credential that matters is the shared one between the MCP server and the service, and it says nothing about the human who asked.

To be fair, there is no authorization being done here at all. It is purely authentication. And honestly, this is where a lot of teams start with a lot of services.

So where does this actually make sense? A few places. There are backend services you don't own that only accept a pre-shared token. If that's what the service insists on, that's what you're stuck with. There are also services where you genuinely don't care about who the caller is. A weather service is the classic toy example. "Who is asking for the weather?" is not a question anyone is trying to answer. Enterprise equivalents exist: a long-running log that accepts writes from any trusted caller, a read-only reference service where the data is intentionally public.

The common denominator is that data-security concerns are low. That's the only place this pattern belongs at scale. Past POC, in any enterprise with meaningful user-specific data, this is not the right answer. There are too many better options beyond it. But it's worth naming as level one all the same.

## Pattern 2: Identity parameter

![Pattern 2 diagram: MCP server sends API key plus X-User-Id header to backend service](/blog/exploring-agent-auth/pattern-2.svg)

<details>
<summary>Code and links</summary>

**Repo:** [`patterns/p02_identity_param`](https://github.com/The-CarL/exploring-agent-auth/tree/main/patterns/p02_identity_param) · [notebook](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p02_identity_param/notebook.ipynb) · [`mcp_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p02_identity_param/mcp_auth.py) · [`service_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p02_identity_param/service_auth.py)

**`mcp_auth.py`** (MCP side):

```python
class IdentityParamHandler(AuthHandler):
    async def prepare_request(self, user_context, headers):
        headers["X-API-Key"] = SHARED_SERVICE_API_KEY
        user = user_context.get("user")
        if user:
            headers["X-User-Id"] = user
        return headers
```

**`service_auth.py`** (service side):

```python
async def get_expense_identity(request: Request) -> Identity:
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != EXPECTED_API_KEY:
        return Identity(method="none", detail="invalid or missing API key")

    user_id = request.headers.get("x-user-id")
    if not user_id:
        return Identity(method="api_key",
                        detail="valid API key but no X-User-Id header")
    return Identity(
        method="string_id",
        user_id=user_id,
        detail="API key verified caller; X-User-Id accepted on trust (no crypto proof)",
    )
```

</details>

This pattern is directly informed by the archetype I described a few sections back: the team with elevated credentials, a backend data service they own, no authorization layer in front of it, no web service in between, no central identity with agreed-upon claims and scopes. It's not a healthy situation. I would not recommend my enterprise customers do this. And it still comes up a surprising amount.

Back to the database example. A team has a database they want to expose through an MCP server, and they want authorization in mind. The simplest thing you can do is bake the authorization mechanism into the tool parameters. Pass the username (or group, or whatever identity element you have) as a parameter to the tool, and use that parameter on the service side to enforce authorization.

This is bad for two reasons.

One, you've effectively built your own authorization layer. That means you are now on the hook for it. If your filtering logic has a bug, that bug is a security bug. This connects back to the point I made in the tiers section: someone always has to own authorization. It is never nobody's job. In this setup, that someone is this team, and the surface area is every filter and every SQL-adjacent join they stitch together by hand.

Two, the identity parameter is trivially easy to spoof. There is no cryptographic guarantee that the "Carlo" in the parameter is actually Carlo. If the agent calling the tool is compromised, or the agent is just running in "do anything" mode, it can pass Steve's name or anyone else's. The service has no way to verify who the actual caller is.

When is this appropriate? Honestly, I struggle to name a case. I'd actually rank this pattern lower than Pattern 1. Pattern 1 at least has honest use cases where user identity doesn't matter. Pattern 2 is saying "we need user identity, and we're going to do it halfway." If you need user identity for authorization, do it all the way. Don't smuggle it through a tool parameter.

## Pattern 3: Inline claim authorization (agent-side)

![Pattern 3 diagram: MCP server reads JWT claims and narrows query parameters, service only sees API key](/blog/exploring-agent-auth/pattern-3.svg)

<details>
<summary>Code and links</summary>

**Repo:** [`patterns/p03_inline_claim_agent`](https://github.com/The-CarL/exploring-agent-auth/tree/main/patterns/p03_inline_claim_agent) · [notebook](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p03_inline_claim_agent/notebook.ipynb) · [`mcp_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p03_inline_claim_agent/mcp_auth.py) · [`service_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p03_inline_claim_agent/service_auth.py)

**`mcp_auth.py`** (MCP side, abridged):

```python
class InlineClaimAgentHandler(AuthHandler):
    def __init__(self):
        self._last_extra_params: dict | None = None

    async def prepare_request(self, user_context, headers):
        headers["X-API-Key"] = SHARED_SERVICE_API_KEY
        jwt = user_context.get("jwt")
        if not jwt:
            return headers

        # Read claims from the JWT to narrow the tool call
        claims = decode_jwt(jwt)
        role = claims.get("role")
        department = claims.get("department")

        # Hand-coded narrowing rules. In practice this logic lives in the
        # agent's system prompt or tool-calling layer.
        if role == "admin":
            pass  # admins see everything
        elif role == "manager" and department:
            self._last_extra_params = {"department": department}

        return headers
```

**`service_auth.py`** (service side): identical to pattern 1. The service only sees the API key. It has no idea the query was narrowed on the way in.

</details>

Pattern 3 is where things start to get a little more serious. This is the first pattern that uses JWTs.

A JWT is a JSON Web Token. It's a way of encoding information about a user that an identity provider has authenticated: the user's identity, plus attributes the system chose to include. The shape of a JWT is not something you get to decide at the application layer. It's configured at the identity service, and that is always a combination of three moving pieces: the identity service itself, the way you requested the token, and whatever identity provider is ultimately backing the thing.

To make this concrete: Amazon Cognito is one place you might generate JWTs. Cognito itself is the token issuer, but a Cognito user pool can be backed by a completely different identity source. The rabbit hole gets deep, and I will not pretend to be an identity expert. A lot of why I wanted to write this post in the first place was to push myself further into this space.

What makes JWTs powerful is the third section of the token. A JWT has three parts, and the last one is a cryptographic signature. If you trust the identity provider's public key, you can verify that this JWT was actually issued by that provider. It's the same concept as certificate verification: public/private key signing, which tells you the token is genuine and wasn't forged.

In this pattern, the user authenticates somewhere (a web app, whatever the front door is), receives a JWT, and passes it to the MCP server. The MCP server decodes the JWT, reads claims like role and department, and uses those claims to narrow the tool call before forwarding the request to the backend. In the repo, the MCP decodes without verifying the signature because the demo focuses on the narrowing step. In real code, you'd verify. Either way, the important detail is that the MCP reads claims and narrows, and the backend service still only sees the pre-shared API key.

Concretely: I, Carlo, call the tool with my JWT. The MCP server decodes it, sees `department=engineering`, and passes `?dept=engineering` to the backend. The backend happily filters by department without knowing why, and without knowing who asked.

This is the first pattern where we get real user-specific authorization, even if only at the narrowing level. When would you actually use it? Narrow situations. You don't control the backend service, and the backend only accepts pre-shared API keys or user-attribute filtering. If you're stuck in that world, this is a way to push user context into the request without the service ever verifying it.

The weakness is exactly that: the service verifies nothing. It is still trusting whatever the MCP server decides to pass.

## Pattern 4: External authorization, agent-side (OPA)

![Pattern 4 diagram: MCP server checks OPA policy before forwarding request with API key to backend service](/blog/exploring-agent-auth/pattern-4.svg)

<details>
<summary>Code and links</summary>

**Repo:** [`patterns/p04_external_authz_agent`](https://github.com/The-CarL/exploring-agent-auth/tree/main/patterns/p04_external_authz_agent) · [notebook](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p04_external_authz_agent/notebook.ipynb) · [`mcp_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p04_external_authz_agent/mcp_auth.py) · [`service_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p04_external_authz_agent/service_auth.py) · [`agent_side.rego`](https://github.com/The-CarL/exploring-agent-auth/tree/main/infra)

**`mcp_auth.py`** (MCP side):

```python
class AgentSideOPAHandler(AuthHandler):
    async def before_tool_call(self, user_context, tool_name):
        jwt = user_context.get("jwt")
        if not jwt:
            raise AuthorizationDenied("no JWT provided")

        claims = decode_jwt(jwt)
        opa_input = {"input": {
            "user": {
                "role": claims.get("role"),
                "department": claims.get("department"),
                "reports_to": claims.get("reports_to"),
            },
            "tool": tool_name,
            "action": "approve" if tool_name == "approve_expense" else "read",
        }}
        r = httpx.post(
            f"{OPA_URL}/v1/data/agentauth/agent_side/decision",
            json=opa_input, timeout=5.0,
        )
        r.raise_for_status()
        decision = r.json().get("result") or {}
        if not decision.get("allow"):
            raise AuthorizationDenied(
                f"OPA denied {user_context.get('user')} calling {tool_name}: "
                f"{decision.get('reason', 'no reason')}"
            )
        return True

    async def prepare_request(self, user_context, headers):
        headers["X-API-Key"] = SHARED_SERVICE_API_KEY
        return headers
```

**`service_auth.py`** (service side): identical to pattern 1. The OPA check happens at the MCP server before the request is sent. The service has no way to verify that any authorization occurred.

</details>

Pattern 4 is where we finally introduce a proper authorization layer. Up to this point, the ladder has been: no authorization, attribute-as-parameter, JWT-claim narrowing. Each of those relies on code in the MCP server to encode the rules. Pattern 4 asks a different question: what if we had a central place that knows the rules?

That is where tools like OPA, Oso, or Cedar come in. These are policy engines with dedicated languages for expressing rich authorization scenarios. And they are not only for user permissions. A very common OPA use case has nothing to do with users at all: network firewall rules. When should this packet be allowed through? When should this network transmission be blocked? That is an authorization decision, and OPA is happy to make it.

Here, we use OPA the way most people first reach for it. The MCP server takes the user's JWT, keeps all the cryptographic benefits of that token, and asks OPA a straightforward question: "can this user run `approve_expense`?" OPA answers yes or no, and the MCP either forwards the tool call or rejects it.

The benefit is flexibility. You have a central system for rules. Configurability and evolvability are high. The rules live in their own language instead of being scattered through your agent code. The downside is everything that comes with "central system": maintenance, integration, and a second source of truth that someone has to keep honest.

What I have seen customers and engineering teams do in practice is build an asynchronous process whose only job is to keep the OPA policy set in sync with facts about the business. You define rules in terms of AD groups, user geographies, department membership, reporting lines, whatever matters. Some of those facts live somewhere already (AD, HR systems). Others don't. An example I've run into: "every user in China can do X, every user in the US can do Y." That geography constraint may not be cleanly encoded in any upstream system, so your sync job has to materialize it into OPA. Someone has to own and nurture that job.

One more thing, and it applies to any dedicated authorization system. The blast radius of a failure is huge. The best-case failure is "users can't do the things they're supposed to be able to do," which is an outage. The worst-case failure is "users can do things they should never have been able to do," which is a breach. A centralized authorization system is not just another service. Treat it that way.

## Pattern 5: JWT passthrough

![Pattern 5 diagram: MCP server passes user JWT to backend service, service validates via JWKS](/blog/exploring-agent-auth/pattern-5.svg)

<details>
<summary>Code and links</summary>

**Repo:** [`patterns/p05_jwt_passthrough`](https://github.com/The-CarL/exploring-agent-auth/tree/main/patterns/p05_jwt_passthrough) · [notebook](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p05_jwt_passthrough/notebook.ipynb) · [`mcp_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p05_jwt_passthrough/mcp_auth.py) · [`service_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p05_jwt_passthrough/service_auth.py)

**`mcp_auth.py`** (MCP side):

```python
class JWTPassthroughHandler(AuthHandler):
    async def prepare_request(self, user_context, headers):
        jwt = user_context.get("jwt")
        if jwt:
            headers["Authorization"] = f"Bearer {jwt}"
        return headers
```

**`service_auth.py`** (service side, the key validation step):

```python
async def _validate_jwt(request, service_client_id, ...):
    auth_header = request.headers.get("authorization")
    token = auth_header.split(" ", 1)[1].strip()

    # Verify signature using Keycloak's JWKS endpoint
    signing_key = jwk_client.get_signing_key_from_jwt(token)
    claims = pyjwt.decode(
        token, signing_key.key,
        algorithms=["RS256"],
        issuer=EXPECTED_ISSUER,
        options={"verify_aud": False},
    )

    # Flag broad-audience tokens so we can distinguish them later
    audiences = claims.get("aud") or []
    is_scoped = audiences == [service_client_id]
    method = "scoped_jwt" if is_scoped else "jwt"

    return Identity(
        method=method,
        user_id=claims.get("preferred_username"),
        claims=claims,
        detail=f"aud={audiences}; azp={claims.get('azp')}",
    )
```

</details>

I have been wanting to poke holes at this one for a while. When agents really came online (in my experience, that was 2024 into 2025) and MCP was already well established, JWT passthrough was always the first thing thrown out for identity propagation. This is the standard way. This is step zero. And it's kind of true, and it's kind of not.

Let's rewind to what a JWT actually is. A JWT is a token an identity provider issues on behalf of a user, with attributes and claims that downstream systems can use. Those downstream uses include authorization, but also things like deciding what to render on a UI. The property that matters most for this pattern is that a JWT is typically minted with an audience in mind. The identity provider is saying "I issued this token for Carlo, to be used with this specific system." Audience is a security boundary, and it is a meaningful one.

Concrete example. I go to Jira, configure an OAuth2 app, and use it to mint a token for a user. Assuming standard setup, that token is minted with Jira as the audience. The identity provider has told every other consumer: this token is for Jira, do not honor it anywhere else. Most systems respect that, and that is a huge part of the security model.

Here is where JWT passthrough starts to break down. If a single JWT is being forwarded to multiple backend services, one of two things has to be true. Either you are generating a different token for each service you touch, in which case the "just pass it through" framing gets a lot more complicated. Or you have lowered the audience-validation bar across all your downstream services so they accept tokens that were not minted for them. That is a real security downgrade, and it is very easy to do without realizing the tradeoff you just made.

Second, you are flinging a high-privilege token around your system. If any of the services in the chain gets compromised, the attacker ends up holding a token that works everywhere you told the ecosystem to accept it.

Third, and this is the one I keep seeing in the wild: token bloat. To make this pattern work across many services, you end up requesting more and more claims and scopes at the moment you mint the token, so every downstream consumer has what it needs. Identity services and web services both have header-size limits for good reasons. You do not want a 20 MB header. Kilobytes is the neighborhood. But when teams take JWT passthrough seriously across enough services, the token keeps growing to accommodate the next downstream consumer.

You would be surprised how many customers are still trying to make this pattern work. I have been on the other side of conversations where the ask was "can you raise the header-size limit on your platform?" and my follow-up was always "have you looked at the overall authorization design here? What are you actually stuffing into that token?" The answer was almost always "everything under the sun." That's the tell. The moment you are arguing with your platform for bigger headers, this pattern has already failed you.

## Pattern 6: Token exchange (RFC 8693)

![Pattern 6 diagram: MCP server exchanges user JWT for scoped token via Keycloak, sends narrowed token to backend service](/blog/exploring-agent-auth/pattern-6.svg)

<details>
<summary>Code and links</summary>

**Repo:** [`patterns/p06_token_exchange`](https://github.com/The-CarL/exploring-agent-auth/tree/main/patterns/p06_token_exchange) · [notebook](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p06_token_exchange/notebook.ipynb) · [`mcp_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p06_token_exchange/mcp_auth.py) · [`service_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p06_token_exchange/service_auth.py)

**`mcp_auth.py`** (MCP side):

```python
class TokenExchangeHandler(AuthHandler):
    def __init__(self):
        self._current_tool_name: str | None = None

    async def before_tool_call(self, user_context, tool_name):
        self._current_tool_name = tool_name
        return True

    async def prepare_request(self, user_context, headers):
        jwt = user_context.get("jwt")
        if jwt:
            target_audience = TOOL_TO_TARGET_CLIENT.get(self._current_tool_name)
            exchanged = exchange_token(jwt, target_audience)
            headers["Authorization"] = f"Bearer {exchanged}"
        return headers
```

**`service_auth.py`** (service side): identical JWKS validation to pattern 5. The difference is what arrives: the exchanged token has `aud` scoped to just this service, so the service records `method="scoped_jwt"`. The magic happened at the MCP server, not here.

</details>

Here is where we start getting into gold-standard territory. Patterns 6, 7, and 8 are where the design stops compromising on the hard parts.

We have talked about what JWTs contain, what you can extract from them to inform authorization decisions, and what happens when you try to use them carelessly (Pattern 5). Token exchange is the next move. It is still efficient, it still propagates user identity, and it honors least privilege in a way passthrough fundamentally cannot.

Here is the idea. Instead of forwarding the user's original broadly-scoped JWT, the MCP server exchanges it with the identity provider for a narrower, service-specific token. The identity element, "here is Carlo, here are some basic attributes about him," stays. But the token the backend receives has `aud` set to exactly that backend, and nothing else. If a downstream service needs additional privileges, the MCP goes back to the identity provider and asks for a new scoped token for that service specifically.

This solves the audience problem directly. The backend receives a token that was minted for it, so audience validation can be strict. It also solves token bloat. You don't have to cram every claim under the sun into the original token, because each downstream service receives its own narrow token with only what it needs.

Someone is still on the hook for the actual authorization decision. I said this in the beginning and I'll say it until I'm blue in the face: someone is always on the hook for authorization. In this pattern, the backend is on the hook. It receives a scoped token, it validates the signature, it reads the claims, and it makes the call based on what's in there. But now the call is being made on a token that was actually minted for this specific service, by the identity provider, and that changes the whole trust model.

This is the pattern I am seeing customers lean into most right now. And I think they are right to.

## Pattern 7: Tool-side external authorization (ReBAC)

![Pattern 7 diagram: backend service validates JWT and checks OPA for per-resource authorization decisions](/blog/exploring-agent-auth/pattern-7.svg)

<details>
<summary>Code and links</summary>

**Repo:** [`patterns/p07_external_authz_tool`](https://github.com/The-CarL/exploring-agent-auth/tree/main/patterns/p07_external_authz_tool) · [notebook](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p07_external_authz_tool/notebook.ipynb) · [`mcp_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p07_external_authz_tool/mcp_auth.py) · [`service_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p07_external_authz_tool/service_auth.py) · [`tool_side.rego`](https://github.com/The-CarL/exploring-agent-auth/tree/main/infra)

**`mcp_auth.py`** (MCP side): identical to pattern 5. Forward the user's JWT as a Bearer token. The fine-grained check happens on the service.

**`service_auth.py`** (service side, the delta from pattern 5):

```python
async def get_expense_identity(request: Request) -> Identity:
    """Validate JWT, then stash OPA URL for tool-side authz later."""
    identity = await _validate_jwt(request, EXPENSE_SERVICE_CLIENT_ID, "_expense")
    if identity.claims is not None:
        identity.claims["_opa_url"] = OPA_URL
    return identity

# The approve_expense route later reads claims["_opa_url"] and calls OPA
# with (caller=bob, target_owner=alice) to decide per-resource authorization.
# OPA's tool_side.rego encodes relationship rules: manages, department peers,
# self-access, admin override.
```

</details>

Pattern 7 is a blend of several earlier patterns. Before getting into it, I want to flag something: the patterns in this post are not mutually exclusive. They are capabilities you can and should combine. Pattern 7 is a good illustration.

The core move is taking the authorization decision out of the agent layer and putting it at the backend service. The user has an identity. It propagates through the MCP server and on to the backend. At the backend, the service itself validates the identity and asks OPA to make a per-resource authorization decision. "Can bob approve alice's expense?" is not a role question. It is a relationship question: does bob manage alice, are they department peers, is there an admin override. That is ReBAC, relationship-based access control, and OPA is comfortable with it.

Worth calling out: you should combine this with token exchange from Pattern 6. The diagram for this pattern does not show token exchange, but there is no reason to forgo it. You still want scoped tokens. You still want narrow audiences. The Pattern 7 delta is about where the final authorization decision happens, not a reason to give up everything Pattern 6 buys you.

I am a big believer that authorization lives closest to the service. That is my opinion, not a universal truth. The trade-off worth thinking about is tool exposure. What if the design intent is to expose different tools to different users based on identity? What if bob should see `approve_expense` as a tool option but alice should not even be told it exists? I have not seen that pattern much in practice, but I can believe it's a legitimate choice. My own preference is the opposite. Expose a broad set of tools and let the agent handle the authorization errors when a user invokes one they are not allowed to use. It keeps the tool surface consistent and moves the authorization decisions somewhere they can actually be verified.

## Pattern 8: Three-legged OAuth (consent)

![Pattern 8 diagram: user consents via browser, Keycloak issues token directly, agent removed from credential chain](/blog/exploring-agent-auth/pattern-8.svg)

<details>
<summary>Code and links</summary>

**Repo:** [`patterns/p08_three_legged_oauth`](https://github.com/The-CarL/exploring-agent-auth/tree/main/patterns/p08_three_legged_oauth) · [notebook](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p08_three_legged_oauth/notebook.ipynb) · [`mcp_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p08_three_legged_oauth/mcp_auth.py) · [`service_auth.py`](https://github.com/The-CarL/exploring-agent-auth/blob/main/patterns/p08_three_legged_oauth/service_auth.py)

**`mcp_auth.py`** (MCP side):

```python
class ThreeLeggedOAuthHandler(AuthHandler):
    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    async def prepare_request(self, user_context, headers):
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers


# The notebook sets auth_handler.access_token after the user completes the
# browser-based PKCE auth code exchange. The agent never sees the user's
# password and never holds a broadly-scoped token.
auth_handler = ThreeLeggedOAuthHandler()
```

**`service_auth.py`** (service side): identical JWKS validation to pattern 5. On the wire, this token is indistinguishable from a pattern 5 or 6 token. The difference is out-of-band: the user explicitly consented through their browser, and the agent was never in possession of user credentials.

</details>

Pattern 8 is more nuanced than the others, and it addresses a question we've been stepping around all along: how did the user get a JWT in the first place?

Every pattern so far assumed the user already had a valid token sitting in their context. That token had to come from somewhere. Three-legged OAuth is the flow that produces it, with a crucial property: the user explicitly consents to what the agent is allowed to do before the token is ever minted. This is the pattern I'm seeing more identity providers and agent platforms lean into as the default.

To some extent, this is less about authorization and more about a different approach to authentication. What makes it matter for authorization is what happens at the consent step. The user is not just proving they are themselves. They are actively deciding which permissions the agent gets to act on their behalf. "Yes, this app can read my expenses. No, this app cannot approve them." The set of scopes the final token carries is literally shaped by what the user agreed to, in a browser, looking at a consent screen, with a direct relationship between them and the identity provider.

You still need authorization at the backend service. Three-legged OAuth does not replace Pattern 7. The backend still receives a JWT, still validates it, still calls OPA for fine-grained decisions. What changes is the origin and shape of the token. Before, the token carried whatever broad permissions the identity provider chose to grant. Now, it carries exactly what the user consciously consented to for this specific agent. That is a meaningfully different trust story, and in my view it is the right end state for agents acting on behalf of real users.

## What's next

Like I said at the start, this has been bouncing around in my head for a while. It has come up in so many of my own conversations that I wanted to nail it down. I actually built the Forge entry quite a while ago. Writing the corresponding post forced me to think about these concepts again, and in doing so there are a handful of explanations I'm already unhappy with. Don't be surprised if a Part 2 shows up.

A few threads I intentionally did not pull in this post, because each deserves its own walkthrough: the first-class authentication and authorization capabilities being built into the MCP spec itself, the A2A protocol, capability tokens, mTLS, gateway identity injection, and the nuances of scope design. Every one of those could be its own runnable Forge entry.

I have a backlog of other Forge projects queued up, too. Some of them will turn into products. Some of them are just me messing around. If you want to follow along, or if you want to push back on something in this post, a few ways to reach me: email, LinkedIn, a comment below, or opening an issue on the [companion repo](https://github.com/The-CarL/exploring-agent-auth).

I hope you got value out of this. I know I did.
