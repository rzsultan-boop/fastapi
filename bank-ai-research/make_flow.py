#!/usr/bin/env python3
"""Flow graph for the Bank Leumi commercial loan-origination use case.

Design rules (applied for clarity, not decoration):
- Okabe-Ito COLORBLIND-SAFE palette throughout.
- Every meaning is REDUNDANTLY encoded: never hue alone — also glyph / line-style / label.
  * forward flow  = solid grey arrow, down the centre
  * rework loop   = dashed orange arrow on the right, numbered R#
  * concentration OVERRIDE = thick dashed purple, labelled
  * status tags   = glyph + word (+ colour as a secondary cue)
- Minimal chartjunk: one subtle shadow for figure/ground grouping; nothing else ornamental.
"""

# Okabe-Ito colorblind-safe palette
INK      = "#111111"
GREY     = "#7a7a7a"   # forward arrows / template
ORANGE   = "#D55E00"   # vermillion — rework loops
PURPLE   = "#CC79A7"   # reddish-purple — concentration override
GREEN    = "#009E73"   # bluish-green — confirmed
BLUE     = "#0072B2"
SKY      = "#56B4E9"
AMBER    = "#E69F00"

W, H = 1240, 1500

# title, leumi role/person, system line, accent, status(tag key)
stages = [
    ("1 · Relationship Manager (intake)", "Business / “Corporate” Division — Liat Shov (ליאת שוב)",
     "CRM → Salesforce", BLUE, "confirmed"),
    ("2 · Credit Analyst / Underwriting", "Corporate-credit underwriters (Business Division)",
     "Loan-origination + spreading → nCino · Moody’s CreditLens · SAS", BLUE, "template"),
    ("3 · Fraud & Financial-Crime (AML / KYC)", "Compliance & AML function — incumbent not named",
     "AML / monitoring → NICE Actimize (fraud)", AMBER, "partial"),
    ("4 · Legal — collateral · covenants · docs", "Legal / collateral counsel",
     "Collateral & covenant management → Finastra", AMBER, "template"),
    ("5 · Pricing / Terms (risk-based)", "Business Division + Finance",
     "Pricing engine inside the origination system", SKY, "template"),
    ("6 · Portfolio / SECTOR-CONCENTRATION & limits", "Risk Management Division (CRO) — Ronen Mori (רונן מורי)",
     "Limits & exposure → portfolio mgmt + risk data warehouse", PURPLE, "confirmed"),
    ("7 · Credit Committee (decision / conditions)", "Credit committee → escalates to Risk Div. / mgmt",
     "Workflow + Credit-Memo module", INK, "template"),
]

# status tag: glyph + label + colour (colour is the SECONDARY cue)
TAGS = {
    "confirmed": ("✓", "CONFIRMED · LEUMI", GREEN),
    "partial":   ("◐", "PARTIAL",           AMBER),
    "template":  ("○", "PEER TEMPLATE",      GREY),
    "gap":       ("!", "GAP",                ORANGE),
}

BX, BW, BH = 70, 600, 108
top, step = 196, 168
box_y = [top + i * step for i in range(len(stages))]
mid = [y + BH / 2 for y in box_y]
right = BX + BW

# rework loops: (label, src_idx, tgt_idx, lane_x, kind, text)
loops = [
    ("R1", 1, 0, 720, "rework",   "incomplete financials → request more"),
    ("R2", 2, 1, 772, "rework",   "AML flag → enhanced due diligence"),
    ("R3", 3, 1, 836, "rework",   "collateral defect → re-underwrite"),
    ("R4", 5, 4, 720, "override", "limit breach → re-price / downsize / decline"),
    ("R5", 6, 1, 910, "rework",   "committee returns conditions"),
]

s = []
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Segoe UI, Helvetica, Arial, sans-serif">')
s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

s.append('<defs>')
for name, col in [("fwd", GREY), ("rw", ORANGE), ("ov", PURPLE)]:
    s.append(f'<marker id="{name}" markerWidth="11" markerHeight="11" refX="8" refY="4" orient="auto">'
             f'<path d="M0,0 L9,4 L0,8 z" fill="{col}"/></marker>')
s.append('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
         '<feDropShadow dx="0" dy="1.5" stdDeviation="2.5" flood-color="#111" flood-opacity="0.16"/></filter>')
s.append('</defs>')

# header
s.append(f'<text x="{BX}" y="52" font-size="31" font-weight="700" fill="{INK}">Bank Leumi — Commercial Loan Origination</text>')
s.append(f'<text x="{BX}" y="82" font-size="17" fill="#444">An iterative, multi-department workflow · roles · people · systems</text>')

# "how to read" legend (redundant encodings spelled out)
ly = 108
s.append(f'<rect x="{BX}" y="{ly}" width="{W-2*BX}" height="64" rx="9" fill="#f6f6f6" stroke="#d8d8d8"/>')
# forward
s.append(f'<line x1="{BX+18}" y1="{ly+24}" x2="{BX+58}" y2="{ly+24}" stroke="{GREY}" stroke-width="3" marker-end="url(#fwd)"/>')
s.append(f'<text x="{BX+66}" y="{ly+29}" font-size="13.5" fill="#333">forward step</text>')
# rework
s.append(f'<line x1="{BX+190}" y1="{ly+24}" x2="{BX+230}" y2="{ly+24}" stroke="{ORANGE}" stroke-width="2.4" stroke-dasharray="7 5" marker-end="url(#rw)"/>')
s.append(f'<text x="{BX+238}" y="{ly+29}" font-size="13.5" fill="#333">rework loop (R#)</text>')
# override
s.append(f'<line x1="{BX+400}" y1="{ly+24}" x2="{BX+440}" y2="{ly+24}" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="3 4" marker-end="url(#ov)"/>')
s.append(f'<text x="{BX+448}" y="{ly+29}" font-size="13.5" fill="#333">concentration override</text>')
# tag glyphs row
tx = BX + 18
s.append(f'<text x="{tx}" y="{ly+51}" font-size="13" fill="#333">status:</text>')
tx += 56
for key in ("confirmed", "partial", "template", "gap"):
    g, lab, col = TAGS[key]
    s.append(f'<text x="{tx}" y="{ly+51}" font-size="14" font-weight="700" fill="{col}">{g}</text>')
    s.append(f'<text x="{tx+16}" y="{ly+51}" font-size="12.5" fill="#333">{lab}</text>')
    tx += 30 + 8.2 * len(lab) + 26

# forward arrows
for i in range(len(stages) - 1):
    x = BX + BW / 2
    s.append(f'<line x1="{x}" y1="{box_y[i]+BH}" x2="{x}" y2="{box_y[i+1]-4}" stroke="{GREY}" stroke-width="3" marker-end="url(#fwd)"/>')

# stage boxes
for i, (title, role, system, accent, status) in enumerate(stages):
    y = box_y[i]
    hl = i == 5
    s.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{BH}" rx="13" fill="#ffffff" '
             f'stroke="{accent}" stroke-width="{3.5 if hl else 1.8}" filter="url(#sh)"/>')
    s.append(f'<rect x="{BX}" y="{y}" width="10" height="{BH}" rx="5" fill="{accent}"/>')
    s.append(f'<text x="{BX+28}" y="{y+32}" font-size="18" font-weight="700" fill="{INK}">{title}</text>')
    s.append(f'<text x="{BX+28}" y="{y+59}" font-size="15" fill="#1f1f1f">{role}</text>')
    s.append(f'<text x="{BX+28}" y="{y+84}" font-size="14" fill="#555">{system}</text>')
    g, lab, col = TAGS[status]
    txt = f"{g} {lab}"
    pw = 8.6 * len(txt) + 20
    s.append(f'<rect x="{right-pw-14}" y="{y+BH-32}" width="{pw}" height="23" rx="11.5" fill="{col}" opacity="0.13"/>')
    s.append(f'<text x="{right-pw-14+pw/2}" y="{y+BH-16}" font-size="12.5" font-weight="700" fill="{col}" text-anchor="middle">{txt}</text>')

# rework / override loops on the right
def loop_path(sy, ty, lane):
    r = 12
    return (f'M {right} {sy} H {lane-r} Q {lane} {sy} {lane} {sy-r} '
            f'V {ty+r} Q {lane} {ty} {lane-r} {ty} H {right+6}')
for label, src, tgt, lane, kind, text in loops:
    sy, ty = mid[src], mid[tgt]
    if kind == "override":
        col, marker, wd, dash = PURPLE, "ov", 4, "3 4"
    else:
        col, marker, wd, dash = ORANGE, "rw", 2.4, "7 5"
    s.append(f'<path d="{loop_path(sy, ty, lane)}" fill="none" stroke="{col}" stroke-width="{wd}" '
             f'stroke-dasharray="{dash}" marker-end="url(#{marker})"/>')
    lyc = (sy + ty) / 2
    s.append(f'<circle cx="{lane}" cy="{lyc}" r="15" fill="{col}"/>')
    s.append(f'<text x="{lane}" y="{lyc+5}" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">{label}</text>')
    s.append(f'<text x="{lane+22}" y="{lyc+5}" font-size="12.5" fill="#333">{text}</text>')

# final node
fy = box_y[-1] + BH + 44
s.append(f'<text x="{BX+BW/2}" y="{fy}" font-size="15.5" font-weight="700" fill="{BLUE}" text-anchor="middle">→ back to Relationship Manager → customer</text>')

# regulatory footer
ry = fy + 30
s.append(f'<rect x="{BX}" y="{ry}" width="{W-2*BX}" height="62" rx="10" fill="#eaf7f1" stroke="{GREEN}" stroke-width="1.5"/>')
s.append(f'<text x="{BX+20}" y="{ry+25}" font-size="13.5" font-weight="700" fill="#0a7a59">✓ Regulatory driver of the concentration step [CONFIRMED · LEUMI]</text>')
s.append(f'<text x="{BX+20}" y="{ry+47}" font-size="13" fill="#0a5e46">Bank of Israel Proper Conduct Directives 311 (credit-risk mgmt) · 313 (single borrower/group limits) · 315.   US OCC 25%-of-capital rule = analogous template.</text>')

s.append('</svg>')

with open("bank-ai-research/loan-flow.svg", "w") as f:
    f.write("\n".join(s))
with open("bank-ai-research/loan-flow.html", "w") as f:
    f.write(f'<!doctype html><meta charset="utf-8"><body style="margin:0">{"".join(s)}</body>')
print("wrote", W, H)
