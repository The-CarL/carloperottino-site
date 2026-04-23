#!/usr/bin/env python3
"""Generate diagrams for the exploring-agent-auth post.

Produces 9 SVGs in public/blog/exploring-agent-auth/.

Run from the repo root:
    python3 scripts/gen_diagrams.py
"""

from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "blog" / "exploring-agent-auth"

WIDTH = 1200
MARGIN = 50
BOX_W = 150
BOX_H = 44
ACTOR_Y = 18
FONT = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

C_STROKE = "#1e1e1e"
C_TEXT = "#1e1e1e"
C_LIFELINE = "#adb5bd"
C_PURPLE = "#6741d9"
C_GREEN = "#2b8a3e"
C_RED = "#c92a2a"

ACTOR_COLORS = {
    "user": "#a5d8ff",
    "browser": "#74c0fc",
    "agent": "#b2f2bb",
    "mcp": "#ffec99",
    "keycloak": "#d0bfff",
    "opa": "#d0bfff",
    "backend": "#ffc9c9",
}

FOOTER_V = {
    "red": ("#fff5f5", "#fa5252", "#c92a2a"),
    "orange": ("#fff4e6", "#fd7e14", "#d9480f"),
    "green": ("#ebfbee", "#40c057", "#2b8a3e"),
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


class D:
    def __init__(self, actors):
        self.actors = actors
        self.rows = []
        self.footer = None
        n = len(actors)
        # columns positioned so actor boxes stay fully within the viewBox
        avail = WIDTH - 2 * MARGIN - BOX_W
        spacing = avail / (n - 1) if n > 1 else 0
        x0 = MARGIN + BOX_W / 2
        self.x = {k: x0 + i * spacing for i, (k, _, _) in enumerate(actors)}

    def msg(self, a, b, text="", dashed=False, color=None, h=36):
        self.rows.append(("msg", a, b, text, dashed, color, h))

    def note(self, a, lines, h=None):
        if isinstance(lines, str):
            lines = [lines]
        h = h or (18 + 16 * len(lines))
        self.rows.append(("note", a, None, lines, False, None, h))

    def note_span(self, a, b, lines, h=None):
        if isinstance(lines, str):
            lines = [lines]
        h = h or (18 + 16 * len(lines))
        self.rows.append(("note_span", a, b, lines, False, None, h))

    def div(self, text, color=C_PURPLE, h=40):
        self.rows.append(("div", None, None, text, False, color, h))

    def spacer(self, h=12):
        self.rows.append(("spacer", None, None, None, False, None, h))

    def foot(self, text, variant="red"):
        self.footer = (text, variant)

    def render(self) -> str:
        LT = ACTOR_Y + BOX_H
        y = LT + 18
        for r in self.rows:
            y += r[6]
        LE = y + 10
        FOOT_H = 46
        FOOT_Y = LE + 16
        TOTAL = FOOT_Y + FOOT_H + 18 if self.footer else LE + 18

        out = []
        out.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {TOTAL}" width="{WIDTH}" height="{TOTAL}">'
        )
        out.append(
            f'<rect x="0" y="0" width="{WIDTH}" height="{TOTAL}" fill="#ffffff"/>'
        )
        out.append(f'<g font-family="{FONT}" fill="{C_TEXT}">')

        # Actor boxes
        for key, label, ck in self.actors:
            x = self.x[key] - BOX_W / 2
            c = ACTOR_COLORS[ck]
            out.append(
                f'<rect x="{x:.1f}" y="{ACTOR_Y}" width="{BOX_W}" height="{BOX_H}" rx="8" ry="8" '
                f'fill="{c}" stroke="{C_STROKE}" stroke-width="1.5"/>'
            )
            out.append(
                f'<text x="{self.x[key]:.1f}" y="{ACTOR_Y + BOX_H / 2 + 5}" text-anchor="middle" '
                f'font-size="14" font-weight="600">{esc(label)}</text>'
            )

        # Lifelines
        for key, _, _ in self.actors:
            out.append(
                f'<line x1="{self.x[key]:.1f}" y1="{LT}" x2="{self.x[key]:.1f}" y2="{LE}" '
                f'stroke="{C_LIFELINE}" stroke-width="1" stroke-dasharray="4 4"/>'
            )

        # Rows
        y = LT + 18
        for kind, a, b, payload, dashed, color, h in self.rows:
            if kind == "msg":
                out.append(self._msg(a, b, payload, dashed, color, y + h / 2))
            elif kind == "note":
                out.append(self._note(a, payload, y, h))
            elif kind == "note_span":
                out.append(self._note_span(a, b, payload, y, h))
            elif kind == "div":
                out.append(self._div(payload, color, y + h / 2))
            y += h

        # Footer
        if self.footer:
            out.append(self._footer(FOOT_Y, FOOT_H))

        out.append("</g>")
        out.append("</svg>")
        return "\n".join(out)

    def _msg(self, a, b, text, dashed, color, y):
        x1 = self.x[a]
        x2 = self.x[b]
        direction = 1 if x2 > x1 else -1
        stroke = color or C_STROKE
        dasharray = ' stroke-dasharray="6 4"' if dashed else ""
        # Inset from lifeline a bit, leave room for arrowhead at destination
        x1_inset = x1 + direction * 4
        x2_inset = x2 - direction * 6
        line = (
            f'<line x1="{x1_inset:.1f}" y1="{y:.1f}" x2="{x2_inset:.1f}" y2="{y:.1f}" '
            f'stroke="{stroke}" stroke-width="1.6"{dasharray}/>'
        )
        ah = 7
        hx1 = x2_inset - direction * ah
        head = (
            f'<polyline points="{hx1:.1f},{y - ah / 1.4:.1f} {x2_inset:.1f},{y:.1f} '
            f'{hx1:.1f},{y + ah / 1.4:.1f}" fill="none" stroke="{stroke}" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        label = ""
        if text:
            lbl_x = (x1 + x2) / 2
            label = (
                f'<text x="{lbl_x:.1f}" y="{y - 7:.1f}" text-anchor="middle" '
                f'font-size="12" fill="{stroke}">{esc(text)}</text>'
            )
        return f"<g>{line}{head}{label}</g>"

    def _note(self, a, lines, y, h):
        cx = self.x[a]
        maxw = max(len(line) for line in lines)
        w = max(180, int(maxw * 7.0) + 26)
        x = cx - w / 2
        # clamp so the note stays inside the viewBox
        if x < MARGIN / 2:
            x = MARGIN / 2
        if x + w > WIDTH - MARGIN / 2:
            x = WIDTH - MARGIN / 2 - w
        text_cx = x + w / 2
        parts = [
            f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" '
            f'fill="#f8f9fa" stroke="{C_STROKE}" stroke-width="1"/>'
        ]
        for i, line in enumerate(lines):
            ly = y + 15 + i * 16
            parts.append(
                f'<text x="{text_cx:.1f}" y="{ly}" text-anchor="middle" font-size="12" '
                f'fill="{C_TEXT}">{esc(line)}</text>'
            )
        return "\n".join(parts)

    def _note_span(self, a, b, lines, y, h):
        x1 = min(self.x[a], self.x[b])
        x2 = max(self.x[a], self.x[b])
        cx = (x1 + x2) / 2
        w = (x2 - x1) + 60
        x = cx - w / 2
        parts = [
            f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" '
            f'fill="#f8f9fa" stroke="{C_STROKE}" stroke-width="1"/>'
        ]
        for i, line in enumerate(lines):
            ly = y + 15 + i * 16
            parts.append(
                f'<text x="{cx:.1f}" y="{ly}" text-anchor="middle" font-size="12" '
                f'fill="{C_TEXT}">{esc(line)}</text>'
            )
        return "\n".join(parts)

    def _div(self, text, color, y):
        x1 = MARGIN
        x2 = WIDTH - MARGIN
        parts = [
            f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" '
            f'stroke-width="1" stroke-dasharray="6 4" opacity="0.5"/>'
        ]
        label_w = max(140, len(text) * 7 + 24)
        lx = MARGIN + 20
        parts.append(
            f'<rect x="{lx}" y="{y - 12}" width="{label_w}" height="24" rx="12" ry="12" '
            f'fill="#ffffff" stroke="{color}" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{lx + label_w / 2:.1f}" y="{y + 4}" text-anchor="middle" '
            f'font-size="12" font-weight="600" fill="{color}">{esc(text)}</text>'
        )
        return "\n".join(parts)

    def _footer(self, y, h):
        text, variant = self.footer
        bg, border, tc = FOOTER_V[variant]
        x = MARGIN
        w = WIDTH - 2 * MARGIN
        parts = [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" ry="6" '
            f'fill="{bg}" stroke="{border}" stroke-width="1.5"/>'
        ]
        parts.append(
            f'<text x="{WIDTH / 2:.1f}" y="{y + h / 2 + 5}" text-anchor="middle" '
            f'font-size="14" font-weight="600" fill="{tc}">{esc(text)}</text>'
        )
        return "\n".join(parts)


# ---------- Pattern definitions ----------

CORE4 = [("user", "User", "user"), ("agent", "Agent", "agent"),
         ("mcp", "MCP Server", "mcp"), ("backend", "Backend Service", "backend")]


def pattern_1():
    d = D(CORE4)
    d.msg("user", "agent", '"What expenses do I have?"')
    d.msg("agent", "mcp", "Tool call (no user context)")
    d.note("mcp", "Attaches shared API key")
    d.msg("mcp", "backend", "X-API-Key: dev-shared-api-key")
    d.note("backend", [
        "Validates API key  ✓",
        "No user identity  ✗",
        "Returns ALL data (unfiltered)",
    ])
    d.msg("backend", "mcp", "All expenses (unfiltered)", dashed=True)
    d.msg("agent", "user", "Response", dashed=True)
    d.foot("Authz: NONE. Service has no user context, everyone sees everything.", "red")
    return d.render()


def pattern_2():
    d = D(CORE4)
    d.msg("user", "agent", '"What expenses do I have?"')
    d.msg("agent", "mcp", "Tool call + user_context(alice)")
    d.note("mcp", ["Attaches API key +", "username header"])
    d.msg("mcp", "backend", "X-API-Key + X-User-Id: alice")
    d.note("backend", [
        "Validates API key  ✓",
        "Reads X-User-Id header",
        "Filters by username",
    ])
    d.msg("backend", "mcp", "Alice's expenses only", dashed=True)
    d.msg("agent", "user", "Response", dashed=True)
    d.foot("Authz: HEADER-BASED. Service trusts asserted username with no cryptographic proof.", "orange")
    return d.render()


def pattern_3():
    d = D(CORE4)
    d.msg("user", "agent", '"What expenses do I have?"')
    d.msg("agent", "mcp", "Tool call + user JWT")
    d.note("mcp", [
        "Decodes JWT (unverified)",
        "Reads role=manager",
        "Narrows query params",
    ])
    d.msg("mcp", "backend", "X-API-Key + ?dept=engineering")
    d.note("backend", [
        "Validates API key  ✓",
        "Returns filtered data",
        "Does NOT know why it was narrowed",
    ])
    d.msg("backend", "mcp", "Engineering dept expenses", dashed=True)
    d.msg("agent", "user", "Response", dashed=True)
    d.foot("Authz: AGENT-SIDE CLAIM NARROWING. MCP reads JWT claims, service cannot verify.", "orange")
    return d.render()


def pattern_4():
    actors = [("user", "User", "user"), ("agent", "Agent", "agent"),
              ("mcp", "MCP Server", "mcp"), ("opa", "OPA", "opa"),
              ("backend", "Backend Service", "backend")]
    d = D(actors)
    d.div("Flow A: alice (employee) requests approval", color=C_RED)
    d.msg("user", "agent", '"Approve alice\'s expense"')
    d.msg("agent", "mcp", "approve_expense + JWT")
    d.msg("mcp", "opa", "role=employee, approve_expense?", color=C_PURPLE)
    d.msg("opa", "mcp", "DENY", dashed=True, color=C_RED)
    d.msg("mcp", "agent", "403 Forbidden", dashed=True, color=C_RED)
    d.note("backend", "Service never called")
    d.div("Flow B: bob (manager) requests approval", color=C_GREEN)
    d.msg("user", "agent", '"Approve alice\'s expense"')
    d.msg("agent", "mcp", "approve_expense + JWT")
    d.msg("mcp", "opa", "role=manager, approve_expense?", color=C_PURPLE)
    d.msg("opa", "mcp", "ALLOW  ✓", dashed=True, color=C_GREEN)
    d.msg("mcp", "backend", "X-API-Key (no user identity)")
    d.msg("backend", "mcp", "Expense approved", dashed=True)
    d.msg("agent", "user", '"Expense approved"', dashed=True)
    d.foot("Authz: OPA AT AGENT LAYER. Rules externalized, service still blind. If MCP is compromised, OPA is skippable.", "orange")
    return d.render()


CORE5 = [("user", "User", "user"), ("agent", "Agent", "agent"),
         ("mcp", "MCP Server", "mcp"), ("keycloak", "Keycloak", "keycloak"),
         ("backend", "Backend Service", "backend")]


def pattern_5():
    d = D(CORE5)
    d.msg("user", "agent", '"What expenses do I have?"')
    d.msg("agent", "mcp", "Tool call + user JWT")
    d.note("mcp", "Passes JWT as-is (no API key)")
    d.msg("mcp", "backend", "Authorization: Bearer <jwt>")
    d.msg("backend", "keycloak", "Validate JWT signature (JWKS)", color=C_PURPLE)
    d.msg("keycloak", "backend", "Signature valid  ✓", dashed=True, color=C_GREEN)
    d.note("backend", [
        "Extracts claims from JWT",
        "role, department, username",
        "aud=[expense, document] (broad)",
    ])
    d.msg("backend", "mcp", "Alice's expenses", dashed=True)
    d.msg("agent", "user", "Response", dashed=True)
    d.foot("Authz: SERVICE-VERIFIED via JWKS. Crypto proof of identity, but broad audience means confused deputy risk.", "green")
    return d.render()


def pattern_6():
    d = D(CORE5)
    d.msg("user", "agent", '"What expenses do I have?"')
    d.msg("agent", "mcp", "Tool call + user JWT")
    d.note("mcp", "Exchanges for scoped token")
    d.msg("mcp", "keycloak", "Token exchange (RFC 8693), aud=expense-svc", color=C_PURPLE)
    d.msg("keycloak", "mcp", "Scoped JWT (aud=[expense-svc], azp=agent)", dashed=True, color=C_PURPLE)
    d.msg("mcp", "backend", "Authorization: Bearer <scoped-jwt>")
    d.msg("backend", "keycloak", "Validate JWT (JWKS)", color=C_PURPLE)
    d.msg("keycloak", "backend", "Valid  ✓", dashed=True, color=C_GREEN)
    d.note("backend", [
        "aud scoped to THIS service  ✓",
        "azp=agent-client (audit trail)",
    ])
    d.msg("backend", "mcp", "Alice's expenses", dashed=True)
    d.msg("agent", "user", "Response", dashed=True)
    d.foot("Authz: SERVICE-VERIFIED + SCOPED TOKEN. Blast radius limited to one service, azp provides audit trail.", "green")
    return d.render()


def pattern_7():
    actors = [("user", "User (bob)", "user"), ("agent", "Agent", "agent"),
              ("mcp", "MCP Server", "mcp"), ("keycloak", "Keycloak", "keycloak"),
              ("backend", "Backend Service", "backend"), ("opa", "OPA", "opa")]
    d = D(actors)
    d.msg("user", "agent", '"Approve alice\'s expense"')
    d.msg("agent", "mcp", "approve_expense + bob's JWT")
    d.msg("mcp", "backend", "Authorization: Bearer <jwt>")
    d.msg("backend", "keycloak", "Validate JWT (JWKS)", color=C_PURPLE)
    d.msg("keycloak", "backend", "Valid  ✓", dashed=True, color=C_GREEN)
    d.note("backend", "caller=bob, target_owner=alice")
    d.msg("backend", "opa", "Can bob approve alice's expense?", color=C_PURPLE)
    d.note("opa", "bob manages alice  ✓")
    d.msg("opa", "backend", "ALLOW  ✓", dashed=True, color=C_GREEN)
    d.msg("backend", "mcp", "Expense approved", dashed=True)
    d.msg("agent", "user", '"Expense approved"', dashed=True)
    d.foot("Authz: SERVICE-VERIFIED JWT + OPA ReBAC. Per-resource decisions based on relationship graph.", "green")
    return d.render()


def pattern_8():
    actors = [("user", "User", "user"), ("browser", "Browser", "browser"),
              ("keycloak", "Keycloak", "keycloak"), ("agent", "Agent", "agent"),
              ("mcp", "MCP Server", "mcp"), ("backend", "Backend Service", "backend")]
    d = D(actors)
    d.div("Phase 1: User consent (out-of-band)", color=C_PURPLE)
    d.msg("user", "browser", "Opens consent URL")
    d.msg("browser", "keycloak", "Authorization request (PKCE)", color=C_PURPLE)
    d.msg("keycloak", "browser", "Consent screen", dashed=True, color=C_PURPLE)
    d.msg("user", "browser", "Grants consent  ✓", color=C_GREEN)
    d.msg("browser", "keycloak", "Auth code exchange", color=C_PURPLE)
    d.msg("keycloak", "agent", "Access token delivered to agent", color=C_GREEN)
    d.note("agent", ["Agent receives token", "Never sees user credentials"])
    d.div("Phase 2: Agent invocation with consent token", color=C_GREEN)
    d.msg("user", "agent", '"What expenses do I have?"')
    d.msg("agent", "mcp", "Tool call + consent JWT")
    d.msg("mcp", "backend", "Authorization: Bearer <jwt>")
    d.note("backend", "Validates JWT via JWKS  ✓")
    d.msg("backend", "mcp", "Alice's expenses", dashed=True)
    d.msg("agent", "user", "Response", dashed=True)
    d.foot("Authz: USER-CONSENTED. Agent removed from credential chain, user controls what the agent can access.", "green")
    return d.render()


# ---------- Architecture diagram ----------

def architecture():
    """Two-lane view: User -> Agent -> (Expense|Document) MCP -> FastAPI.

    Shared infrastructure (Keycloak, OPA) shown below the main flow.
    """
    W = 1200
    # Layout columns (left to right): user, agent, mcp, service
    col_x = {"user": 100, "agent": 300, "mcp": 560, "service": 900}
    box_w = 150
    top_y = 60  # center y of top lane (expense)
    bot_y = 170  # center y of bottom lane (document)
    box_h = 56
    H = 380
    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
    )
    out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')
    out.append(f'<g font-family="{FONT}" fill="{C_TEXT}">')

    mid_y = (top_y + bot_y) / 2

    def box(cx, cy, w, h, label_lines, fill):
        x = cx - w / 2
        y = cy - h / 2
        out.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="10" ry="10" '
            f'fill="{fill}" stroke="{C_STROKE}" stroke-width="1.5"/>'
        )
        if isinstance(label_lines, str):
            label_lines = [label_lines]
        n = len(label_lines)
        for i, ln in enumerate(label_lines):
            ly = cy + (i - (n - 1) / 2) * 16 + 5
            out.append(
                f'<text x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="14" '
                f'font-weight="600">{esc(ln)}</text>'
            )

    def arrow(x1, y1, x2, y2, color=C_STROKE):
        import math
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L == 0:
            return
        ux, uy = dx / L, dy / L
        # shorten start and end to avoid overlapping boxes
        sx = x1 + ux * 4
        sy = y1 + uy * 4
        ex = x2 - ux * 8
        ey = y2 - uy * 8
        out.append(
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>'
        )
        # arrowhead
        ah = 9
        # perpendicular
        px, py = -uy, ux
        h1x = ex - ux * ah + px * ah * 0.5
        h1y = ey - uy * ah + py * ah * 0.5
        h2x = ex - ux * ah - px * ah * 0.5
        h2y = ey - uy * ah - py * ah * 0.5
        out.append(
            f'<polyline points="{h1x:.1f},{h1y:.1f} {ex:.1f},{ey:.1f} {h2x:.1f},{h2y:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round"/>'
        )

    # User, Agent (single boxes, centered vertically)
    box(col_x["user"], mid_y, box_w, box_h, "User", ACTOR_COLORS["user"])
    box(col_x["agent"], mid_y, box_w, box_h, "Agent", ACTOR_COLORS["agent"])

    # Top lane: Expense MCP + Expense FastAPI
    box(col_x["mcp"], top_y, box_w, box_h, ["Expense", "MCP Server"], ACTOR_COLORS["mcp"])
    box(col_x["service"], top_y, box_w, box_h, ["Expense", "FastAPI Service"], ACTOR_COLORS["backend"])

    # Bottom lane: Document MCP + Document FastAPI
    box(col_x["mcp"], bot_y, box_w, box_h, ["Document", "MCP Server"], ACTOR_COLORS["mcp"])
    box(col_x["service"], bot_y, box_w, box_h, ["Document", "FastAPI Service"], ACTOR_COLORS["backend"])

    # Arrows
    arrow(col_x["user"] + box_w / 2, mid_y, col_x["agent"] - box_w / 2, mid_y)
    # Agent branches to both MCPs
    arrow(col_x["agent"] + box_w / 2, mid_y - 6, col_x["mcp"] - box_w / 2, top_y)
    arrow(col_x["agent"] + box_w / 2, mid_y + 6, col_x["mcp"] - box_w / 2, bot_y)
    # MCP to Service per lane
    arrow(col_x["mcp"] + box_w / 2, top_y, col_x["service"] - box_w / 2, top_y)
    arrow(col_x["mcp"] + box_w / 2, bot_y, col_x["service"] - box_w / 2, bot_y)

    # Shared infrastructure panel
    panel_y = 260
    panel_h = 90
    panel_x = 100
    panel_w = W - 2 * panel_x
    out.append(
        f'<rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="{panel_h}" '
        f'rx="8" ry="8" fill="#f8f9fa" stroke="{C_LIFELINE}" stroke-width="1" '
        f'stroke-dasharray="6 4"/>'
    )
    out.append(
        f'<text x="{panel_x + 16}" y="{panel_y + 22}" font-size="12" font-weight="600" '
        f'fill="#495057">SHARED INFRASTRUCTURE</text>'
    )
    # Two small boxes inside the panel
    sp_y = panel_y + 58
    kc_cx = panel_x + 220
    opa_cx = panel_x + 720
    box(kc_cx, sp_y, 140, 40, "Keycloak", ACTOR_COLORS["keycloak"])
    out.append(
        f'<text x="{kc_cx + 80}" y="{sp_y + 5}" font-size="12" fill="#495057">'
        f'identity, JWKS, token exchange</text>'
    )
    box(opa_cx, sp_y, 140, 40, "OPA", ACTOR_COLORS["opa"])
    out.append(
        f'<text x="{opa_cx + 80}" y="{sp_y + 5}" font-size="12" fill="#495057">'
        f'policy decisions (role + relationship)</text>'
    )

    out.append("</g></svg>")
    return "\n".join(out)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diagrams = {
        "architecture.svg": architecture(),
        "pattern-1.svg": pattern_1(),
        "pattern-2.svg": pattern_2(),
        "pattern-3.svg": pattern_3(),
        "pattern-4.svg": pattern_4(),
        "pattern-5.svg": pattern_5(),
        "pattern-6.svg": pattern_6(),
        "pattern-7.svg": pattern_7(),
        "pattern-8.svg": pattern_8(),
    }
    for name, svg in diagrams.items():
        path = OUT_DIR / name
        path.write_text(svg)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
