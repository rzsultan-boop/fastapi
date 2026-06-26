# Bank AI-Adoption Research — Checkpoint

> Working checkpoint. Saved to survive session/container loss. Confidence tags:
> **[HIGH]** multi-source verified · **[MED]** single/soft source · **[GAP]** not found.
> Tagging for the loan use-case: **[CONFIRMED-LEUMI]** / **[PEER-BANK TEMPLATE]** / **[GENERIC ASSUMPTION]**.

Last updated: 2026-06-26. Status: **both passes COMPLETE.** Full Leumi loan-origination use-case written to `LEUMI-loan-origination-usecase.md` (this folder).

**Pass-2 added (Leumi org chain, [CONFIRMED-LEUMI / HIGH]):**
- **CRO** = Head of Risk Management Division = **Ronen Mori** (רונן מורי), since Jan 2023 (prev: Liat Shov 2020–23; Bosmat Ben-Tzvi before).
- **Head of Corporate/Commercial Credit** = Head of Business/"Corporate" Division = **Liat Shov** (ליאת שוב), since Jan 2023 (prev: Ronen Agassi → left to CEO Migdal).
- **CIO** = Technology Division = **Chaim Skolnik** (חיים שקולניק), named Dec 2020 — 2026 tenure unconfirmed [MED].
- Gaps still open: Head of Compliance/AML, CISO, current CIO re-confirmation, and which LOS/rating/limits vendors Leumi actually runs (only Salesforce CRM + Actimize fraud confirmed).
- System/process template (nCino, Moody's CreditLens, OCC handbook, 12 CFR Part 30 App. D) = [PEER-BANK TEMPLATE], not Leumi-confirmed.

---

## PART 1 — People to talk to (AI adoption / startup partnering)

Goal: who a startup should approach as the bank's relevant rep for partnering on AI adoption — owner of AI strategy / current state, or warm-introducer to the decision-maker. Mirrors the Leumi mapping (Tal Homsky, CDO).

### Bank Leumi (reference / already known)
| Person | Title | Notes |
|---|---|---|
| **Tal Homsky** (טל חומסקי) | CDO | Previously flagged. Reference anchor. |

### Bank Hapoalim (בנק הפועלים)
AI run **centrally** as a strategic enterprise program — no startup accelerator vehicle found.

| Person | Title | LinkedIn | Confidence |
|---|---|---|---|
| **Gadi Ganon** (גדי גנון) | Chief AI Officer / Head of Data & AI dept. ex-Playtika VP AI; ex-8200 (~20-25y). Reports to Rachmil. | linkedin.com/in/gadi-ganon-14081220a | **[HIGH]** (3-0) |
| **Erez Rachmil** (ארז רחמיל) | Deputy CEO & Head of Technology Division (eff. Mar 2025). Exec sponsor/champion of AI rollout. ex-Playtika CTO. | not confirmed | **[HIGH]** (3-0) |

- **Context:** Feb 2026 bank-wide **Microsoft 365 + Copilot** program (~12 cross-divisional projects; "first Israeli bank to embed Copilot bank-wide"). Pitch should complement Copilot, not compete. **[HIGH]**
- **[GAP]** No separate CDO; no named innovation-lab/accelerator lead at Hapoalim.

### Bank Discount (בנק דיסקונט)
Two power centers: internal AI/data/digital owner (Angel) + outward startup arm (Discount Tech). Plus a tech/IT decision-maker (Kaplan).

| Person | Title | LinkedIn | Confidence |
|---|---|---|---|
| **Rachely Miller** (רחלי מילר) ⭐ | Head of Innovation, Bank Discount — owns the bank's **AI strategy roadmap** + **startup collaborations**. Under Idan Angel. **Current incumbent.** Best target: senior, owns AI roadmap, reachable, job = engaging startups. | il.linkedin.com/in/rachely-miller-2954739 | **[HIGH]** (Fintech Week TLV 2025 bio + LinkedIn) |
| **Idan Angel** (עידן אנגל) | EVP / Head of Digital, Data, Innovation, Marketing & CX division. Strategy & budget owner. **Non-technical** (UC Berkeley econ/poli-sci; ex-Bezeq/Colmobil/Hapoalim strategy). | **No personal LinkedIn exists** (the "Idan Angel–Citi" profile is a different person). Role via Discount Bank corporate LinkedIn post. Inferred email pattern (UNVERIFIED): Idan.Angel@dbank.co.il | Role **[HIGH]**; no-LinkedIn **[HIGH]** |
| **Adi Kaplan** (עדי קפלן) | EVP, CIO / Head of Technologies Division (since 2020/21). Real tech-adoption decision-maker; reachable; technical (IDF Signal Corps, CS+MBA, ex-Hapoalim tech, ex-Clal/Clalbit). | linkedin.com/in/adi-kaplan-6392bb28 | **[HIGH]** |
| **Or Hadar** | Data Product Manager & Strategist (working-level under Angel). | linkedin.com/in/or-hadar- | **[MED]** |

**Discount Tech** = the bank's high-tech / VC / ecosystem arm ("one-stop shop for Israeli tech cos from fundraising to maturity"). **This is the investor/partner-to-startups arm, NOT the buyer.** Good as a warm-intro/connector, risky as a sales door (frames you as portfolio prospect).
| Person | Title | LinkedIn |
|---|---|---|
| **Dr. Guy/Gai Navon** (גיא נבון) | CEO, Discount Tech | il.linkedin.com/in/guynavon |
| **Nir Kouris** | CMO, Discount Tech (inbound contact) | linkedin.com/in/nirkouris · **Nir.Kouris@dbank.co.il** |

- **Programs:** D Academy community (w/ TheMarker, Team8, Meitar, EY); a16z collaboration + Israel Founders Mission (NY, June 2026, w/ IDBNY); Miami events.
- **Moved on (don't get mis-pointed):** **Shani Federman** (former Head of BD & Innovation → now CEO of Greenlend, a Discount JV; linkedin.com/in/shani-federman-10543337) and **Yael Waisbourd-Sucary** (former Head of Innovation & Fintech → now Head of Tech, UBS Wealth Israel).
- **Adoption pattern intel:** Discount's flagship GenAI product **"AI Stocktalk"** is powered by external fintech **Bridgewise** → Discount adopts AI via **startup partnerships, not build**. Good proof point.

**Recommended plays:**
- Discount: open with **Rachely Miller** (owns AI roadmap + startup engagement) → warm intro up to **Angel** (budget) / across to **Kaplan** (CIO, if infra/platform product).
- Hapoalim: **Ganon** (technical owner) / **Rachmil** (sponsor).

---

## PART 2 — Bank Leumi commercial loan-origination use case (in progress)

### Confirmed-for-Leumi facts (pass 1)
- **[CONFIRMED-LEUMI] Salesforce CRM** — Leumi deployed cloud Salesforce CRM (~tens of millions ₪; decided end-2013; replaced two prior CRM systems; serves call center). Source: pc.co.il/news/191141. (3-0)
- **[CONFIRMED-LEUMI] NICE Actimize** — present at Leumi for **fraud / real-time transaction monitoring** (2-1). ⚠️ The "this is Leumi's **AML** system" framing was **REFUTED (0-3)** — describe as fraud/transaction-monitoring, not confirmed-AML. Source: finextra.com/newsarticle/15191.
- **[CONFIRMED-LEUMI] Regulatory backbone** — Bank of Israel **Proper Conduct of Banking Business Directives 311** (Credit Risk Management — requires analyzing portfolio composition & identifying risk concentrations), **313** (single borrower/group-of-borrowers limits), **315**. These force the sector-concentration check that can decline/downsize/re-price a loan. (3-0). Sources: boi.org.il (Directive 311/313 pages; primary PDF h2762.pdf).

### Gaps pass 1 could NOT confirm for Leumi (being filled by pass 2 via peer-bank templates)
- Core-banking platform vendor
- Loan-origination system (LOS)
- Credit rating/scoring engine
- Collateral / legal / covenant management system
- Data warehouse / data lake
- Limits & exposure / portfolio-management system
- **Named risk/credit executives** (CRO / Head of Corporate Credit / CISO / Head of Compliance-AML) — exec-roster angle returned empty in pass 1

### Target structure for the final deliverable
Iterative, back-and-forth flow (the centerpiece — show backward kicks):

RM (CRM) ⇄ Credit Analyst/Underwriting ⇄ Fraud & Financial-Crime (AML/KYC) ⇄ Legal (collateral, covenants) ⇄ Pricing/Terms (risk-based) ⇄ **Portfolio/Sector-Concentration & Limits** ⇄ Credit Committee → back to RM.

Backward loops to dramatize: underwriting → RM for more financials; legal → risk on collateral; concentration-limit breach → forces re-pricing / downsizing / decline; committee → returns conditions.

Each step to be annotated with: system (tagged template vs confirmed) + Leumi role/person.

---

## Deliverables already committed & pushed (durable)
- `RESEARCH-CHECKPOINT.md` (this file)
- `LEUMI-loan-origination-usecase.md` — full use-case narrative
- `loan-flow.png` / `loan-flow.svg` / `loan-flow.html` — rendered flow diagram
- `make_flow.py` — diagram generator (re-run: `python3 bank-ai-research/make_flow.py`, then headless-chromium screenshot)

## PRIORITY NOTE (per user, 2026-06-26)
**SYSTEMS matter more than personnel names** for the Leumi pitch — the systems are what our wedge/tech
plugs into. Personnel names are secondary. Technique to find systems: mine current/former Leumi
employees' LinkedIn/CV/skills + Leumi job postings (people & job ads name the exact systems).

## STATUS 2026-06-26 ~18:15 UTC — both passes hit SESSION LIMIT (resets 7:40pm UTC)
- **Org-gaps pass** `wf_a425e9bb-3c2` (w2ub8bd4z): **partial success** — confirmed findings folded into
  use-case doc §5/§5b (Tech Division split → Nir Omer + Shauli Bar Or; Skolnik → core-banking
  subsidiary CEO; Temenos confirmed for *Pepper* only; SAS credit-rating **refuted**).
- **Systems-mining pass (PRIORITY)** `wf_a3537b79-88f` (w7varnj04): FAILED — 0 results (session limit).
  **→ RE-LAUNCHED after reset as `wf_bf48d0da-599` (task wd06d1r8x), ~19:50 UTC.** When it lands, fold
  confirmed SYSTEMS into use-case doc §5b + `make_flow.py`, commit + push. Top open item: commercial
  core, the new future-core subsidiary stack, LOS, credit-rating engine, data warehouse.

### TO RESUME (after 7:40pm UTC reset)
Re-launch the systems-mining mission (employee-profile + job-ad mining for named systems). Spec is in
the git history (commit "prioritize systems-over-names") / the w7varnj04 prompt. Then fold confirmed
SYSTEMS into `LEUMI-loan-origination-usecase.md` §5b AND `make_flow.py`, commit + push.

### Confirmed systems so far (use-case doc §5b has the table)
Salesforce CRM ✓ · NICE Actimize (fraud) ✓ · Temenos (Pepper digital bank only) ✓ · SAS credit-rating ✗ refuted · everything else NOT FOUND.

## Workflow recovery (completed runs)
- Pass 1 (Leumi-direct): run ID `wf_6ef6496b-d83` — completed; synthesis stubbed but verified claims recovered.
- Pass 2 (peer-bank template → Leumi map): run ID `wf_c9f38ba9-160` — completed; names folded into use-case doc.
