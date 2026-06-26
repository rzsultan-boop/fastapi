# Bank Leumi — Commercial Loan Origination as a Multi-Department, Back-and-Forth Use Case

> Purpose: a concrete narrative an AI vendor can use to show where AI helps in an
> iterative, multi-department workflow at **Bank Leumi**.
>
> Every item is tagged:
> - **[CONFIRMED-LEUMI]** — verified for Bank Leumi specifically
> - **[PEER-BANK TEMPLATE]** — how well-documented banks/vendors do it; *analogous*, not proven for Leumi
> - **[GENERIC]** — standard banking logic / assumption
>
> Jurisdiction note: the regulatory *template* below is US OCC/Basel (illustrative). **Leumi's actual
> rulebook is the Bank of Israel Proper Conduct directives** — called out where they apply.

---

## 1. The use case

A mid-market / SME business (say, a construction-materials importer) asks its Bank Leumi
relationship manager for a ₪20M credit facility. What looks to the customer like "submit
documents → get an answer" is internally an **iterative loop** across 6–7 functions, where the
file repeatedly bounces **backward** before it can move forward. The concentration check near the
end can send the whole thing back to re-pricing or kill it — even if the borrower is perfectly
creditworthy on its own.

---

## 2. The flow — and where it goes BACKWARD (the centerpiece)

```
  Relationship Manager (CRM)
        │  ▲
        ▼  │ (R1) underwriting requests more financials/clarifications
  Credit Analyst / Underwriting ──────────────────────────────────┐
        │  ▲                                                       │
        ▼  │ (R2) AML/KYC red flag → back for enhanced due diligence│
  Fraud & Financial-Crime (AML / KYC)                              │
        │  ▲                                                       │
        ▼  │ (R3) legal finds collateral/lien defect → back to risk │
  Legal (collateral, covenants, documentation)                     │
        │                                                          │
        ▼                                                          │
  Pricing / Terms (risk-based pricing) ◄───────────────┐          │
        │                                              │          │
        ▼                                              │ (R4)     │
  PORTFOLIO / SECTOR-CONCENTRATION & LIMITS  ──────────┘ breach → │
        │   forces re-price / downsize / decline                  │
        ▼                                                          │
  Credit Committee ──(R5) returns conditions / more analysis ─────┘
        │
        ▼
  Back to Relationship Manager → customer
```

**The five backward loops that make this a hard, AI-addressable problem:**
- **R1** Underwriting → RM: "financials incomplete / need updated AR aging, guarantor statements."
- **R2** AML → RM/underwriting: beneficial-ownership or sanctions hit → enhanced due diligence.
- **R3** Legal → Risk: collateral/lien defect, missing covenant → re-underwrite security.
- **R4** Concentration → Pricing: sector limit nearly/already breached → re-price up, cut the
  amount, or decline. **This is the loop the user cares about** — the bank may give worse terms or
  say no *because of its existing book*, not the borrower.
- **R5** Credit Committee → back down the chain: approves *with conditions* (more collateral,
  covenants, lower limit), restarting legal/pricing.

---

## 3. Step-by-step: function → system → Leumi role/person

| Step | Function | System (category → product) | Leumi mapping |
|---|---|---|---|
| Intake | Relationship Manager / business banker captures the request, manages the relationship | **CRM** → **Salesforce** **[CONFIRMED-LEUMI]** (cloud Salesforce CRM, deployed ~2014, replaced 2 prior systems) | **Business ("Corporate") Division**, **Liat Shov** (ליאת שוב), Head, since Jan 2023 **[CONFIRMED-LEUMI]** |
| Underwriting | Credit analyst spreads financials, assigns internal risk rating, sets indicative amount/rate | **Loan Origination System + credit analysis** → **nCino** (Spreads), **Moody's CreditLens** (2017; replaced legacy RiskAnalyst), **SAS** **[PEER-BANK TEMPLATE]** — *not confirmed for Leumi* | Corporate/Commercial credit underwriters under the Business Division **[GENERIC mapping]** |
| Financial crime | AML/KYC, beneficial ownership, sanctions, fraud screening | **AML / transaction monitoring** → **NICE Actimize** **[CONFIRMED-LEUMI]** (present at Leumi for **fraud / real-time transaction monitoring**; ⚠️ "Leumi's AML system" framing was *refuted* — treat as fraud/monitoring); peers also use SymphonyAI | **Compliance & AML** function **[GAP — incumbent not named]** |
| Legal | Collateral perfection, covenants, loan documentation | **Collateral & covenant mgmt** → e.g. **Finastra Limit & Collateral Management** **[PEER-BANK TEMPLATE]** | Legal / collateral counsel **[GENERIC mapping]** |
| Pricing | Risk-based pricing from rating + cost of capital | Pricing engine, often inside the **LOS (nCino/CreditLens)** **[PEER-BANK TEMPLATE]** | Business Division + Finance **[GENERIC mapping]** |
| **Concentration** | Check borrower's **sector** vs the bank's existing exposure; enforce limits | **Limits & exposure / portfolio mgmt** → nCino Credit Portfolio Mgmt / Moody's **[PEER-BANK TEMPLATE]**; driven by **risk data warehouse** | **Risk Management Division** (= the CRO function), **Ronen Mori** (רונן מורי), Head, since Jan 2023 **[CONFIRMED-LEUMI]** |
| Approval | Credit committee decision / conditions | Workflow + **Credit Memo** module (nCino / CreditLens) **[PEER-BANK TEMPLATE]** | Credit committee, escalating to Risk Division / management **[GENERIC mapping]** |

---

## 4. Why the concentration step can override a good borrower

**[CONFIRMED-LEUMI / Bank of Israel]** The check is mandated by **BoI Proper Conduct of Banking
Business Directives**:
- **311** — Credit Risk Management: requires analyzing **portfolio composition** and identifying
  **risk concentrations of every kind** (the rule that forces the sector check on each deal).
- **313** — limits on a **single borrower / group of borrowers**.
- **315** — related concentration governance.

**[PEER-BANK / REGULATORY TEMPLATE — US OCC, analogous]** The mechanics of *how* this binds:
- A **"concentration of credit" = exposures exceeding 25% of capital** to one borrower, an affiliated
  group, **or borrowers dependent on one industry** (OCC Comptroller's Handbook). *(US threshold —
  illustrative; Israel's specific ratios live in the BoI directives above.)*
- Limits are **portfolio-level, board-approved**, sitting *above* the individual deal (12 CFR Part 30
  Appendix D, Heightened Standards): aggregated front-line + concentration limits must stay within
  the **risk appetite statement**.
- **Two-directional quarterly monitoring/escalation**: front-line units report limit compliance to
  independent risk management ≥ quarterly; risk management reports profile-vs-appetite and
  concentration compliance to the board ≥ quarterly; **a limit breach is escalated to senior
  management/board** — i.e. the marginal ₪20M loan that tips the importer's sector over the line gets
  bounced up and back down (loop **R4/R5**).

**The "so what" for AI:** the back-and-forth (R1–R5) is exactly the friction — re-keyed data across
CRM/LOS/AML/limits systems, manual financial spreading, committee memos, and concentration math done
late in the process. That's the AI value story: pre-empt the backward loops (complete-file checks,
auto-spreading, early concentration simulation) so deals don't ricochet.

---

## 5. Leumi people map (confirmed vs gap)

| Canonical role | Leumi division | Named person | Confidence |
|---|---|---|---|
| **Chief Risk Officer** | Risk Management Division (ראש חטיבת ניהול סיכונים) | **Ronen Mori** (רונן מורי), since Jan 2023 (prev: Liat Shov 2020–23; Bosmat Ben-Tzvi before) | **[CONFIRMED-LEUMI / HIGH]** |
| **Head of Corporate/Commercial Credit** | Business / "Corporate" Division (ראש החטיבה העסקית) | **Liat Shov** (ליאת שוב), since Jan 2023 (prev: Ronen Agassi → left to CEO Migdal) | **[CONFIRMED-LEUMI / HIGH]** |
| **CIO / Head of Technology** | Technology Division (חטיבת טכנולוגיות) | **Chaim Skolnik** (חיים שקולניק), named Dec 2020 from Cyber — ⚠️ 2026 tenure not re-confirmed | **[CONFIRMED-LEUMI / MED]** |
| **CDO** | (Data) | **Tal Homsky** (טל חומסקי) — from prior mapping | **[carried over]** |
| Head of Compliance & AML | Compliance & AML (ציות ואיסור הלבנת הון) | — | **[GAP]** |
| CISO | Cyber/Infosec | — | **[GAP]** |

Context: CEO **Hanan Friedman** reshuffled 6 of 12 division heads in Dec 2020 (all internal
promotions), which is why several of these chairs turned over in 2020–2023. **[CONFIRMED-LEUMI]**

---

## 6. Open questions / next research
- Current (2026) Leumi **CIO** confirmation (Skolnik is Dec-2020-vintage).
- Named Leumi **Head of Compliance/AML**, **CISO**, **Head of Financial Crime**.
- Confirm **Tal Homsky / CDO** against a current Leumi periodic report and where the CDO sits vs
  Technology and Risk.
- Which **LOS / rating / limits** vendors Leumi *actually* runs beyond confirmed Salesforce + Actimize
  (nCino? Finastra? Temenos? FIS? Moody's? in-house core-native?). **None of the system-template
  vendors are confirmed for Leumi.**

---

### Source anchors
- **Leumi people:** Globes did=1001434953 (Jan 2023 reshuffle: Mori→Risk, Shov→Business); Calcalist
  L-3878585 (Dec 2020 reshuffle); leumi.co.il/en/Profile-Members-of-Management; TAU alumni (Ben-Tzvi=CRO).
- **Leumi systems:** pc.co.il/news/191141 (Salesforce CRM); finextra.com/newsarticle/15191 (Actimize).
- **Regulatory:** boi.org.il Directives 311/313/315; OCC Loan Portfolio Management Comptroller's
  Handbook; 12 CFR Part 30 Appendix D.
- **System templates:** ncino.com (commercial-lending, Spreads, credit-portfolio-management);
  moodysanalytics.com/CreditLens; finastra.com/limit-and-collateral-management.
