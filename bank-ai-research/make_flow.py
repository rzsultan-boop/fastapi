#!/usr/bin/env python3
"""Flow graph: Bank Leumi commercial loan origination — flow · departments · people · systems.

Clarity rules (not decoration):
- Okabe-Ito COLORBLIND-SAFE palette; every meaning REDUNDANTLY encoded (glyph + line-style + label).
- forward = solid grey; rework = dashed orange (R#); concentration override = thick dashed purple.
- SYSTEM status per step is the priority signal: ✓ confirmed-Leumi · ○ peer template · ✗ not found.
- ✓ before a person = role+person confirmed for Leumi.
- Bottom band = the CONFIRMED infrastructure layer (what we actually verified Leumi runs).
"""

INK="#111111"; GREY="#7a7a7a"; ORANGE="#D55E00"; PURPLE="#CC79A7"
GREEN="#009E73"; BLUE="#0072B2"; SKY="#56B4E9"; AMBER="#E69F00"

W, H = 1300, 1660

# title, person, person_confirmed, system, sys_status, accent
stages = [
 ("1 · Relationship Manager (intake)", "Business / “Corporate” Division — Liat Shov (ליאת שוב)", True,
  "CRM → Salesforce", "confirmed", BLUE),
 ("2 · Credit Analyst / Underwriting", "Corporate-credit underwriters (Business Division)", False,
  "Loan-origination + spreading  (template: nCino · Moody’s CreditLens)", "template", BLUE),
 ("3 · Fraud & Financial-Crime (AML / KYC)", "Compliance & AML function", False,
  "Fraud / monitoring → NICE Actimize", "confirmed", AMBER),
 ("4 · Legal — collateral · covenants · docs", "Legal / collateral counsel", False,
  "Collateral & covenant mgmt  (template: Finastra)", "template", AMBER),
 ("5 · Pricing / Terms (risk-based)", "Business Division + Finance", False,
  "Pricing engine inside the origination system", "template", SKY),
 ("6 · Portfolio / SECTOR-CONCENTRATION & limits", "Risk Management Division (CRO) — Ronen Mori (רונן מורי)", True,
  "Limits & exposure + data warehouse", "notfound", PURPLE),
 ("7 · Credit Committee (decision / conditions)", "Credit committee → escalates to Risk Div. / mgmt", False,
  "Workflow + Credit-Memo module", "template", INK),
]

SYS = {  # glyph, label, colour
 "confirmed": ("✓", "SYSTEM CONFIRMED", GREEN),
 "template":  ("○", "PEER TEMPLATE",    GREY),
 "notfound":  ("✗", "SYSTEM NOT FOUND", ORANGE),
}

BX, BW, BH = 70, 640, 112
top, step = 214, 170
box_y=[top+i*step for i in range(len(stages))]; mid=[y+BH/2 for y in box_y]; right=BX+BW

loops=[("R1",1,0,772,"rework","incomplete financials → request more"),
       ("R2",2,1,824,"rework","AML flag → enhanced due diligence"),
       ("R3",3,1,888,"rework","collateral defect → re-underwrite"),
       ("R4",5,4,772,"override","limit breach → re-price / downsize / decline"),
       ("R5",6,1,962,"rework","committee returns conditions")]

s=[]
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Helvetica, Arial, sans-serif">')
s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
s.append('<defs>')
for n,c in [("fwd",GREY),("rw",ORANGE),("ov",PURPLE)]:
    s.append(f'<marker id="{n}" markerWidth="11" markerHeight="11" refX="8" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="{c}"/></marker>')
s.append('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="1.5" stdDeviation="2.5" flood-color="#111" flood-opacity="0.16"/></filter>')
s.append('</defs>')

s.append(f'<text x="{BX}" y="50" font-size="31" font-weight="700" fill="{INK}">Bank Leumi — Commercial Loan Origination</text>')
s.append(f'<text x="{BX}" y="80" font-size="17" fill="#444">Flow · departments · people · systems — an iterative, back-and-forth workflow</text>')

# legend
ly=104
s.append(f'<rect x="{BX}" y="{ly}" width="{W-2*BX}" height="84" rx="9" fill="#f6f6f6" stroke="#d8d8d8"/>')
s.append(f'<line x1="{BX+18}" y1="{ly+24}" x2="{BX+58}" y2="{ly+24}" stroke="{GREY}" stroke-width="3" marker-end="url(#fwd)"/>')
s.append(f'<text x="{BX+66}" y="{ly+29}" font-size="13.5" fill="#333">forward step</text>')
s.append(f'<line x1="{BX+200}" y1="{ly+24}" x2="{BX+240}" y2="{ly+24}" stroke="{ORANGE}" stroke-width="2.4" stroke-dasharray="7 5" marker-end="url(#rw)"/>')
s.append(f'<text x="{BX+248}" y="{ly+29}" font-size="13.5" fill="#333">rework loop (R#)</text>')
s.append(f'<line x1="{BX+420}" y1="{ly+24}" x2="{BX+460}" y2="{ly+24}" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="3 4" marker-end="url(#ov)"/>')
s.append(f'<text x="{BX+468}" y="{ly+29}" font-size="13.5" fill="#333">concentration override</text>')
s.append(f'<text x="{BX+700}" y="{ly+29}" font-size="13.5" fill="#333">✓ before a person = confirmed for Leumi</text>')
# system-status key
s.append(f'<text x="{BX+18}" y="{ly+58}" font-size="13" fill="#333">system status:</text>')
tx=BX+128
for k in ("confirmed","template","notfound"):
    g,lab,col=SYS[k]
    s.append(f'<text x="{tx}" y="{ly+58}" font-size="14" font-weight="700" fill="{col}">{g}</text>')
    s.append(f'<text x="{tx+17}" y="{ly+58}" font-size="12.5" fill="#333">{lab}</text>')
    tx+=30+8.4*len(lab)+28
s.append(f'<text x="{BX+18}" y="{ly+76}" font-size="11.5" fill="#666">“Peer template” = how comparable banks do it (nCino/CreditLens/Finastra); not verified for Leumi. “Not found” = no Leumi-specific source.</text>')

# forward arrows
for i in range(len(stages)-1):
    x=BX+BW/2
    s.append(f'<line x1="{x}" y1="{box_y[i]+BH}" x2="{x}" y2="{box_y[i+1]-4}" stroke="{GREY}" stroke-width="3" marker-end="url(#fwd)"/>')

# boxes
for i,(title,person,pc,system,st,accent) in enumerate(stages):
    y=box_y[i]; hl=i==5
    s.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{BH}" rx="13" fill="#fff" stroke="{accent}" stroke-width="{3.5 if hl else 1.8}" filter="url(#sh)"/>')
    s.append(f'<rect x="{BX}" y="{y}" width="10" height="{BH}" rx="5" fill="{accent}"/>')
    s.append(f'<text x="{BX+28}" y="{y+31}" font-size="18" font-weight="700" fill="{INK}">{title}</text>')
    pre = '<tspan fill="'+GREEN+'" font-weight="700">✓ </tspan>' if pc else ''
    s.append(f'<text x="{BX+28}" y="{y+58}" font-size="14.5" fill="#1f1f1f">{pre}{person}</text>')
    s.append(f'<text x="{BX+28}" y="{y+85}" font-size="13.5" fill="#555">{system}</text>')
    g,lab,col=SYS[st]; txt=f"{g} {lab}"; pw=8.4*len(txt)+20
    s.append(f'<rect x="{right-pw-14}" y="{y+BH-32}" width="{pw}" height="23" rx="11.5" fill="{col}" opacity="0.14"/>')
    s.append(f'<text x="{right-pw-14+pw/2}" y="{y+BH-16}" font-size="12.5" font-weight="700" fill="{col}" text-anchor="middle">{txt}</text>')

# loops
def lp(sy,ty,lane):
    r=12
    return (f'M {right} {sy} H {lane-r} Q {lane} {sy} {lane} {sy-r} V {ty+r} Q {lane} {ty} {lane-r} {ty} H {right+6}')
for label,src,tgt,lane,kind,text in loops:
    sy,ty=mid[src],mid[tgt]
    col,mk,wd,dash=(PURPLE,"ov",4,"3 4") if kind=="override" else (ORANGE,"rw",2.4,"7 5")
    s.append(f'<path d="{lp(sy,ty,lane)}" fill="none" stroke="{col}" stroke-width="{wd}" stroke-dasharray="{dash}" marker-end="url(#{mk})"/>')
    yc=(sy+ty)/2
    s.append(f'<circle cx="{lane}" cy="{yc}" r="15" fill="{col}"/>')
    s.append(f'<text x="{lane}" y="{yc+5}" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">{label}</text>')
    s.append(f'<text x="{lane+22}" y="{yc+5}" font-size="12.5" fill="#333">{text}</text>')

fy=box_y[-1]+BH+42
s.append(f'<text x="{BX+BW/2}" y="{fy}" font-size="15.5" font-weight="700" fill="{BLUE}" text-anchor="middle">→ back to Relationship Manager → customer</text>')

# infrastructure band (confirmed)
iy=fy+24
s.append(f'<rect x="{BX}" y="{iy}" width="{W-2*BX}" height="96" rx="10" fill="#eef7fb" stroke="{BLUE}" stroke-width="1.6"/>')
s.append(f'<text x="{BX+18}" y="{iy+25}" font-size="14.5" font-weight="700" fill="#0a5a86">✓ Confirmed infrastructure layer (verified for Leumi)</text>')
chips=["AWS (cloud)","Amazon EKS / EKS Anywhere","Amazon Aurora","AllCloud (delivery partner)","GFT → FinTeka open banking","Temenos → Pepper digital bank only"]
cx=BX+18; cyr=iy+44
for c in chips:
    cw=8.0*len(c)+24
    if cx+cw>W-BX-18: cx=BX+18; cyr+=30
    s.append(f'<rect x="{cx}" y="{cyr-15}" width="{cw}" height="23" rx="11.5" fill="#ffffff" stroke="{BLUE}" stroke-width="1"/>')
    s.append(f'<text x="{cx+cw/2}" y="{cyr+1}" font-size="12.5" fill="#0a5a86" text-anchor="middle">{c}</text>')
    cx+=cw+10
s.append(f'<text x="{BX+18}" y="{iy+90}" font-size="11.5" fill="#b25a00">✗ Not found (insider-only): main commercial core · loan/credit system (מערכת אשראי) · credit-rating engine · enterprise data warehouse — Leumi is building a future cloud-native core via a new subsidiary.</text>')

# regulatory footer
ry=iy+96+14
s.append(f'<rect x="{BX}" y="{ry}" width="{W-2*BX}" height="60" rx="10" fill="#eaf7f1" stroke="{GREEN}" stroke-width="1.5"/>')
s.append(f'<text x="{BX+18}" y="{ry+24}" font-size="13.5" font-weight="700" fill="#0a7a59">✓ Regulatory driver of the concentration step [CONFIRMED · LEUMI]</text>')
s.append(f'<text x="{BX+18}" y="{ry+46}" font-size="13" fill="#0a5e46">Bank of Israel Proper Conduct Directives 311 (credit-risk mgmt) · 313 (single borrower/group limits) · 315.   US OCC 25%-of-capital rule = analogous template.</text>')

s.append('</svg>')
open("bank-ai-research/loan-flow.svg","w").write("\n".join(s))
open("bank-ai-research/loan-flow.html","w").write(f'<!doctype html><meta charset="utf-8"><body style="margin:0">{"".join(s)}</body>')
print("wrote",W,H)
