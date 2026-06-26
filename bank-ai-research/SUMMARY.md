# Bank Leumi — Business Loan Origination: People · Departments · Process · Systems
### Research summary for an AI-adoption / startup partnering pitch

**Confidence tags:** `[CONFIRMED-LEUMI]` verified for Leumi · `[TEMPLATE]` peer-bank/industry standard, not verified for Leumi · `[NOT FOUND]` no Leumi-specific source · `[LEAD]` single/unverified source.
Companion files: `LEUMI-loan-origination-usecase.md` (full detail) · `loan-flow.png/.svg` (diagram) · `RESEARCH-CHECKPOINT.md` (provenance).

---

## 1. The business loan process (the use case)

A business / SME applies to Bank Leumi for a credit facility. To the customer it looks like "submit docs → get an answer." Internally it is an **iterative, multi-department loop** where the file repeatedly bounces **backward** before it can move forward. The sector-concentration check near the end can downgrade or kill a perfectly creditworthy deal **because of the bank's existing book**.

**Forward path:**
`Relationship Manager → Credit Analyst/Underwriting → Fraud & Financial-Crime (AML/KYC) → Legal (collateral, covenants) → Pricing/Terms → Portfolio/Sector-Concentration & Limits → Credit Committee → back to RM → customer`

**The five backward loops (the centerpiece — this is the AI-addressable friction):**
| Loop | Bounces back | Why |
|---|---|---|
| **R1** | Underwriting → RM | financials incomplete; request more |
| **R2** | AML → RM/Underwriting | beneficial-owner / sanctions flag → enhanced due diligence |
| **R3** | Legal → Risk | collateral / lien defect → re-underwrite |
| **R4** | **Concentration → Pricing** | **sector limit breached → re-price / downsize / decline** |
| **R5** | Credit Committee → down-chain | approved *with conditions* → restarts legal/pricing |

**AI value story:** the back-and-forth is re-keyed data across CRM/LOS/AML/limits systems, manual financial spreading, and concentration math done too late. AI can pre-empt the loops (complete-file checks, auto-spreading, early concentration simulation) so deals don't ricochet.

---

## 2. Departments & people

| Function (canonical role) | Leumi department | Person | Confidence |
|---|---|---|---|
| Intake / relationship | Business / "Corporate" Division (החטיבה העסקית) | **Liat Shov** (ליאת שוב), Head, since Jan 2023 | `[CONFIRMED-LEUMI]` |
| Credit underwriting | Corporate-credit underwriters (within Business Division) | role — not named | `[TEMPLATE]` |
| Chief Risk Officer / concentration | Risk Management Division (חטיבת ניהול סיכונים) | **Ronen Mori** (רונן מורי), Head/CRO, since Jan 2023 | `[CONFIRMED-LEUMI]` |
| Fraud & Financial-Crime | Compliance & AML (ציות ואיסור הלבנת הון) | **Dr. Nir Yamin** (chief compliance officer, ~Mar 2026; prev. Pini Shatz) | `[LEAD]` |
| Technology — Cyber & Infrastructure | Cyber & Infrastructure Division | **Nir Omer** (ניר עומר), SVP & board | `[CONFIRMED-LEUMI]` |
| Technology — Development | Technological Development Division | **Shauli Bar Or** (שאולי בר אור), SVP & board | `[CONFIRMED-LEUMI]` |
| Future core-banking build | wholly-owned subsidiary (cloud-native core) | **Chaim Skolnik** (חיים שקולניק), CEO (ex-CIO) | `[CONFIRMED-LEUMI]` |
| Data | CDO function | **Tal Homsky** (טל חומסקי) | `[LEAD / carried over]` |
| CISO / Infosec | within Cyber & Infrastructure Div. | likely under Nir Omer (older infosec head: Moshe First) | `[LEAD]` |

**Org note:** CEO **Hanan Friedman** reshuffled division heads (Dec 2020), then **split the single Technology Division** (~Dec 2023) into Cyber & Infrastructure (Omer) and Technological Development (Bar Or) — **eliminating the CIO role** — and spun out a **subsidiary to build a future cloud-native core** (Skolnik). Leumi is mid-core-replacement, a real timing signal for new tech.

---

## 3. Systems (the priority)

### ✅ Confirmed for Leumi
| Layer / category | System | Tag |
|---|---|---|
| CRM | **Salesforce** | `[CONFIRMED-LEUMI]` |
| Fraud / transaction-monitoring | **NICE Actimize** (fraud; "AML" framing unproven) | `[CONFIRMED-LEUMI]` |
| Cloud provider | **AWS** | `[CONFIRMED-LEUMI]` |
| Containers / DevOps | **Amazon EKS + EKS Anywhere** (hybrid); **Amazon Aurora** (some workloads) | `[CONFIRMED-LEUMI]` |
| Cloud delivery partner | **AllCloud** (Solutions Factory / EKS-as-a-Service; CCoE mgr Moti Levi) | `[CONFIRMED-LEUMI]` |
| Open banking | **FinTeka** marketplace, built by **GFT** on serverless AWS (Open API Framework, API Gateway, WAF, Kinesis) | `[CONFIRMED-LEUMI]` |
| Digital-bank core | **Temenos** on **VMware** — **Pepper digital bank only**, not the commercial core | `[CONFIRMED-LEUMI / scoped]` |

### ❌ Not found (the system-of-record layer — insider-only)
| Category | Status |
|---|---|
| Main commercial **core banking** | `[NOT FOUND]` — likely legacy mainframe being replaced by Skolnik's subsidiary |
| **Loan-origination / credit system** (מערכת אשראי) | `[NOT FOUND]` |
| **Credit rating / scoring engine** | `[NOT FOUND]` — SAS attribution **refuted** (0-3); no Moody's/FICO evidence |
| Enterprise **data warehouse / BI** | `[NOT FOUND]` — Amazon Redshift-150TB claim **refuted** (0-3) |
| Limits & collateral, ECM | `[NOT FOUND]` |

### ○ Peer-bank template (how comparable banks do it — not verified for Leumi)
Loan-origination system **nCino**; credit analysis/rating **Moody's CreditLens** (legacy RiskAnalyst); limits & collateral **Finastra**; AML **SymphonyAI**.

> **Takeaway:** Leumi's **modern cloud/AI-infra layer is well-mapped** (AWS/EKS/AllCloud/GFT) — strong if your wedge is cloud/AI/data-platform-adjacent. The **legacy systems of record** are deliberately unpublished; they survived no open source and are best obtained via a warm conversation or insider.

---

## 4. Regulatory driver of the concentration step `[CONFIRMED-LEUMI]`
**Bank of Israel — Proper Conduct of Banking Business Directives:** **311** (credit-risk management — analyze portfolio composition & identify concentrations) · **313** (single borrower / group-of-borrowers limits) · **315**. These force the sector-concentration check (loop R4). *US OCC's 25%-of-capital concentration rule and 12 CFR Part 30 App. D = analogous template, not Leumi's actual rulebook.*

---

## Appendix A — Bank AI-adoption / startup-partnering contacts (the "who to talk to" research)

**Bank Leumi** — Tal Homsky (טל חומסקי), CDO. `[LEAD]`

**Bank Hapoalim** (AI run centrally; no accelerator):
- **Gadi Ganon** (גדי גנון) — Chief AI Officer / Head of Data & AI. linkedin.com/in/gadi-ganon-14081220a `[HIGH]`
- **Erez Rachmil** (ארז רחמיל) — Deputy CEO & Head of Technology; champion of the Feb-2026 Microsoft 365 + Copilot rollout. `[HIGH]`

**Bank Discount** (two power centers + a startup arm):
- **Rachely Miller** (רחלי מילר) ⭐ — Head of Innovation; owns the bank's AI strategy roadmap + startup collaborations. **Best entry point.** il.linkedin.com/in/rachely-miller-2954739 `[HIGH]`
- **Idan Angel** (עידן אנגל) — EVP, Head of Digital/Data/Innovation/Marketing (strategy & budget owner; **no personal LinkedIn**). `[HIGH role]`
- **Adi Kaplan** (עדי קפלן) — EVP, CIO / Head of Technologies (reachable tech decision-maker). linkedin.com/in/adi-kaplan-6392bb28 `[HIGH]`
- **Discount Tech** (VC/ecosystem arm, *not* the buyer) — Dr. Guy Navon (CEO), Nir Kouris (CMO, Nir.Kouris@dbank.co.il). Warm-intro vector only.
- Adoption pattern: flagship GenAI product "AI Stocktalk" is powered by external fintech **Bridgewise** → Discount buys via startup partnerships.

---

## Source anchors
- **People/org:** Globes did=1001434953 (Jan-2023 reshuffle); Calcalist bjgdpobw6 & hjovssiq11g (Tech-Division split, subsidiary); leumi.co.il management page.
- **Systems:** aws.amazon.com/solutions/case-studies/bankleumi-eksa-case-study; allcloud.io/case_studies/bank-leumi; gft.com (FinTeka); Temenos/VMware 2017 PR; pc.co.il/news/191141 (Salesforce); finextra 15191 (Actimize).
- **Regulatory:** boi.org.il Directives 311 / 313 / 315.
