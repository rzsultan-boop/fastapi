# Session Handoff — Bank AI-Adoption / LinkedIn Project

> Purpose of this file: give a **fresh Claude session (zero prior memory)** everything needed to
> continue seamlessly. Read `SUMMARY.md` for findings; this file is the *narrative + context + how-to*.

## 1. What this project is
Business-development research for a startup selling **AI adoption** into Israeli banks. Two threads:
- **Thread A — "who to talk to":** map the people responsible for AI adoption at **Bank Hapoalim** and
  **Bank Discount** (modeled on how **Bank Leumi**'s Tal Homsky / CDO was flagged).
- **Thread B — Leumi commercial loan-origination use case:** a concrete, multi-department, back-and-forth
  process (departments · people · **systems**) the startup can use in demos and intro meetings.

The repo is named `fastapi` only by accident of the container checkout. **Move it into the local
LinkedIn project folder; it is unrelated to FastAPI.**

## 2. What's been delivered (all in `bank-ai-research/`)
| File | Contents |
|---|---|
| `SUMMARY.md` | Consolidated: people, departments, loan process, systems + Hapoalim/Discount contacts appendix |
| `LEUMI-loan-origination-usecase.md` | Full use-case narrative; §5b = systems confirmed/template/not-found |
| `loan-flow.png` / `.svg` / `.html` | The flow diagram (delivered to user) |
| `make_flow.py` | Diagram generator (Python → SVG/HTML; screenshot via headless Chromium) |
| `RESEARCH-CHECKPOINT.md` | Provenance, workflow run IDs, recovery notes |
| `CLAUDE.md` | Project context auto-loaded by a new session |

## 3. Key findings (condensed — see SUMMARY.md for tags/sources)
**Thread A — contacts:**
- **Hapoalim:** Gadi Ganon (Chief AI Officer), Erez Rachmil (Deputy CEO/Tech; Microsoft Copilot rollout).
- **Discount:** **Rachely Miller** ⭐ (Head of Innovation — owns AI roadmap + startup collabs; best entry),
  Idan Angel (EVP Digital/Data/Innovation — **no personal LinkedIn**), Adi Kaplan (CIO), Discount Tech
  (Navon CEO, Kouris CMO — VC/ecosystem arm, warm-intro only, not the buyer).
- **Leumi:** Tal Homsky (CDO).

**Thread B — Leumi loan process & systems:**
- Process: RM → Underwriting → AML/KYC → Legal → Pricing → **Sector-Concentration & limits** → Credit
  Committee → back to RM, with 5 backward loops (R1–R5); R4 = concentration override (decline/downsize/
  re-price a good borrower due to existing sector exposure). Driven by **BoI Directives 311/313/315**.
- People (confirmed): **Liat Shov** (Head, Business/Corporate Division), **Ronen Mori** (CRO/Head of Risk
  Management). Tech Division was **split** into Cyber & Infrastructure (**Nir Omer**) + Technological
  Development (**Shauli Bar Or**); ex-CIO **Chaim Skolnik** now CEO of a **subsidiary building a future
  cloud-native core**. Compliance/AML lead **Dr. Nir Yamin** `[LEAD]`; CISO under Omer `[LEAD]`.
- Systems **CONFIRMED**: Salesforce (CRM), NICE Actimize (fraud), **AWS**, **Amazon EKS/EKS Anywhere**,
  Aurora, **AllCloud** (delivery partner), **GFT → FinTeka** open banking, Temenos→Pepper (digital bank only).
- Systems **NOT FOUND** (insider-only): main commercial core, loan/credit system (מערכת אשראי),
  credit-rating engine, enterprise data warehouse. (Redshift-150TB and SAS attributions were **refuted**.)
- Systems **TEMPLATE** (peer-bank, not Leumi-verified): nCino, Moody's CreditLens, Finastra.

## 4. Open items / next steps
1. **Highest value:** name + tech stack of Skolnik's **future-core subsidiary** (new entity may have its
   own press/LinkedIn). Leumi being mid-core-replacement is a real timing signal.
2. Confirm the **main commercial core** (legacy mainframe/COBOL vs package) — likely insider-only.
3. Verify the `[LEAD]` people: Dr. Nir Yamin (Compliance/AML), CISO, and re-confirm Tal Homsky/CDO.
4. (Thread A) Optional: confirm Discount's current Head-of-Innovation tenure; deepen Hapoalim innovation arm.

## 5. How the research was run (reuse this)
- **Tool:** the `deep-research` workflow (fan-out web search → fetch → 3-vote adversarial verify →
  synthesize). Invoke via the Workflow tool, `name: "deep-research"`, with a detailed `args` prompt.
- **Best technique for systems:** mine **current/former Leumi employees' LinkedIn skills/experience** and
  **Leumi job postings** (they name the exact systems) + **vendor case studies** (AWS/AllCloud/GFT named
  Leumi). This cracked the infra layer when generic search failed.
- **Diagrams:** `make_flow.py` builds an SVG; render with the pre-installed Chromium:
  `python3 make_flow.py` then
  `<chrome> --headless --screenshot=loan-flow.png --window-size=1300,1660 file://…/loan-flow.html`.

## 6. Environment constraints learned (this ran in a cloud container)
- Network policy **blocked** direct fetches to many hosts (snyk.io, github.com clone, leumi.co.il) — only
  the workflow's search path worked. Could NOT download external Claude skills into `~/.claude/skills`.
- Hit a **session/usage limit** mid-research once (resets on a clock); re-ran after reset.
- LinkedIn personal profiles often ungated only via search snippets, not direct fetch.
- Therefore: **save frequently** (commit + push) — done throughout.

## 7. User preferences (carry forward)
- **Systems matter more than personnel names** (the wedge plugs into systems).
- **Minimal fluff**, honest confidence tags, **Hebrew-first** search.
- Wants work **committed & pushed continuously** so nothing is lost.
- Colorblind-safe, redundantly-encoded diagrams.

---
*End of handoff. A new session: read `CLAUDE.md` + this file + `SUMMARY.md`, then pick up from §4.*
