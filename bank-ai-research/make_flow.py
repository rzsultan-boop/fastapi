#!/usr/bin/env python3
"""Generate a styled flow graph (SVG) for the Bank Leumi commercial loan-origination use case."""

W, H = 1180, 1430

stages = [
    # title, leumi role/person, system line, color, tag
    ("1 · Relationship Manager (intake)", "Business / “Corporate” Division — Liat Shov (ליאת שוב)",
     "CRM → Salesforce", "#2563eb", "CONFIRMED-LEUMI"),
    ("2 · Credit Analyst / Underwriting", "Corporate-credit underwriters (Business Division)",
     "LOS + spreading → nCino · Moody’s CreditLens · SAS", "#4f46e5", "TEMPLATE"),
    ("3 · Fraud & Financial-Crime (AML / KYC)", "Compliance & AML function  —  incumbent not named",
     "AML / monitoring → NICE Actimize (fraud)", "#dc2626", "MIXED"),
    ("4 · Legal (collateral · covenants · docs)", "Legal / collateral counsel",
     "Collateral & covenant mgmt → Finastra", "#b45309", "TEMPLATE"),
    ("5 · Pricing / Terms (risk-based)", "Business Division + Finance",
     "Pricing engine inside LOS (nCino / CreditLens)", "#0d9488", "TEMPLATE"),
    ("6 · Portfolio / SECTOR-CONCENTRATION & limits", "Risk Management Division (CRO) — Ronen Mori (רונן מורי)",
     "Limits & exposure → portfolio mgmt + risk DWH", "#7c3aed", "CONFIRMED-LEUMI"),
    ("7 · Credit Committee (decision / conditions)", "Credit committee → escalates to Risk Div. / mgmt",
     "Workflow + Credit Memo module", "#334155", "TEMPLATE"),
]

BX, BW, BH = 70, 560, 104
top, step = 150, 162
box_y = [top + i * step for i in range(len(stages))]
mid = [y + BH / 2 for y in box_y]
right = BX + BW

tag_color = {"CONFIRMED-LEUMI": "#16a34a", "TEMPLATE": "#64748b", "GAP": "#dc2626", "MIXED": "#d97706"}

# backward loops: (label, source_idx, target_idx, lane_x, color, text)
loops = [
    ("R1", 1, 0, 690, "#ef4444", "needs more financials"),
    ("R2", 2, 1, 740, "#ef4444", "AML flag → EDD"),
    ("R3", 3, 1, 800, "#ef4444", "collateral defect → re-underwrite"),
    ("R4", 5, 4, 690, "#9333ea", "limit breach → re-price / downsize / decline"),
    ("R5", 6, 1, 870, "#ef4444", "committee returns conditions"),
]

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Helvetica, Arial, sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#f8fafc"/>')

# arrow markers
svg.append('<defs>')
for name, col in [("fwd", "#94a3b8"), ("back", "#ef4444"), ("back2", "#9333ea")]:
    svg.append(f'<marker id="{name}" markerWidth="11" markerHeight="11" refX="8" refY="4" orient="auto">'
               f'<path d="M0,0 L9,4 L0,8 z" fill="{col}"/></marker>')
svg.append('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
           '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.18"/></filter>')
svg.append('</defs>')

# title
svg.append(f'<text x="{BX}" y="54" font-size="30" font-weight="700" fill="#0f172a">Bank Leumi — Commercial Loan Origination</text>')
svg.append(f'<text x="{BX}" y="84" font-size="17" fill="#475569">A multi-department, back-and-forth workflow · roles · people · systems</text>')
svg.append(f'<text x="{BX}" y="112" font-size="14" fill="#64748b">Solid grey = forward flow   ·   Dashed red = rework loop   ·   Dashed purple = concentration override</text>')

# forward arrows
for i in range(len(stages) - 1):
    x = BX + BW / 2
    svg.append(f'<line x1="{x}" y1="{box_y[i]+BH}" x2="{x}" y2="{box_y[i+1]-4}" stroke="#94a3b8" stroke-width="2.5" marker-end="url(#fwd)"/>')

# stage boxes
for i, (title, role, system, color, tag) in enumerate(stages):
    y = box_y[i]
    hl = i == 5  # highlight concentration
    svg.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{BH}" rx="13" fill="#ffffff" '
               f'stroke="{color}" stroke-width="{3.5 if hl else 2}" filter="url(#sh)"/>')
    svg.append(f'<rect x="{BX}" y="{y}" width="9" height="{BH}" rx="4" fill="{color}"/>')
    svg.append(f'<text x="{BX+26}" y="{y+30}" font-size="17.5" font-weight="700" fill="#0f172a">{title}</text>')
    svg.append(f'<text x="{BX+26}" y="{y+56}" font-size="14.5" fill="#1e293b">{role}</text>')
    svg.append(f'<text x="{BX+26}" y="{y+80}" font-size="13.5" fill="#475569">{system}</text>')
    # tag pill
    tc = tag_color[tag]
    pw = 11 * len(tag) + 22
    svg.append(f'<rect x="{right-pw-14}" y="{y+BH-30}" width="{pw}" height="21" rx="10.5" fill="{tc}" opacity="0.14"/>')
    svg.append(f'<text x="{right-pw-14+pw/2}" y="{y+BH-15}" font-size="11.5" font-weight="700" fill="{tc}" text-anchor="middle">{tag}</text>')

# backward loops (curved on right)
def loop_path(sy, ty, lane):
    r = 12
    return (f'M {right} {sy} H {lane-r} Q {lane} {sy} {lane} {sy-r} '
            f'V {ty+r} Q {lane} {ty} {lane-r} {ty} H {right+6}')
for label, s, t, lane, col, txt in loops:
    sy, ty = mid[s], mid[t]
    marker = "back2" if col == "#9333ea" else "back"
    svg.append(f'<path d="{loop_path(sy, ty, lane)}" fill="none" stroke="{col}" stroke-width="2.3" '
               f'stroke-dasharray="7 5" marker-end="url(#{marker})"/>')
    ly = (sy + ty) / 2
    svg.append(f'<circle cx="{lane}" cy="{ly}" r="15" fill="{col}"/>')
    svg.append(f'<text x="{lane}" y="{ly+5}" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">{label}</text>')
    svg.append(f'<text x="{lane+22}" y="{ly+5}" font-size="12.5" fill="#334155">{txt}</text>')

# final node
fy = box_y[-1] + BH + 46
svg.append(f'<text x="{BX+BW/2}" y="{fy}" font-size="15" font-weight="700" fill="#2563eb" text-anchor="middle">→ back to Relationship Manager → customer</text>')

# regulatory footer
ry = fy + 36
svg.append(f'<rect x="{BX}" y="{ry}" width="{W-2*BX}" height="58" rx="10" fill="#ecfdf5" stroke="#16a34a" stroke-width="1.5"/>')
svg.append(f'<text x="{BX+20}" y="{ry+24}" font-size="13.5" font-weight="700" fill="#15803d">Regulatory driver of the concentration step [CONFIRMED-LEUMI]:</text>')
svg.append(f'<text x="{BX+20}" y="{ry+45}" font-size="13" fill="#166534">Bank of Israel Proper Conduct Directives 311 (credit-risk mgmt) · 313 (single borrower/group limits) · 315. (US OCC 25%-of-capital rule is an analogous template.)</text>')

svg.append('</svg>')

with open("bank-ai-research/loan-flow.svg", "w") as f:
    f.write("\n".join(svg))

html = f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:#f8fafc}}</style></head><body>{"".join(svg)}</body></html>'
with open("bank-ai-research/loan-flow.html", "w") as f:
    f.write(html)
print("wrote svg+html", W, H)
