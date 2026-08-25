# SVT Advisor Copilot — Agentforce Phase 5 build guide

Build plan for extending **SVT Advisor Copilot** after Phases 1–4 and **Path A Data Library**.

**Audience:** Demo builder (Sanjay)  
**Org:** Agentforce + Data 360 Developer Edition  
**Agent:** SVT Advisor Copilot (Employee Agent)

---

## Related docs

| Doc | Purpose |
|---|---|
| [Main demo guide](svt-data-cloud-agentforce-demo.md) | Architecture, Phases 1–4, test matrix |
| [Data Library org setup](svt-data-library-org-setup.md) | Path A PDF + agent wiring |
| [Document grounding reference](svt-rag-pilot-v1-reference.md) | Path A scope (Path B dropped) |
| [Real-time ingestion](svt-realtime-ingestion-guide.md) | Streaming Ingestion API (Karan live demo) |
| [Test ride confirmation email](svt-test-ride-confirmation-email.md) | Email Flow in Create Task |

---

## 1. Current state (built)

| Capability | Status | Mechanism |
|---|---|---|
| Rider retention (Module 1) | Built | Subagents + Data Cloud DMOs + Flows |
| Lead engagement (Module 2) | Built | `SVT Get Lead Context V2`, `Get Lead Intent v2`, `Recommend Dealer`, `Create Lead Test Ride Task` |
| Duplicate task guard | Built | `hasOpenTestRideTask`, `openTaskSubject` on Get Lead Context V2 |
| Confirmation email | Built | `emailSent` on Create Task when `contactPermission=true` |
| Streaming engagement | Built | Ingestion API data stream → Website Engagement DMO |
| Document grounding | Built / in progress | Agent-level **SVT Advisor Quick Guides** Data Library |
| Path B unstructured RAG | **Dropped** | Do not build S3 / UDLO / Search Index |

### Subagents (typical org layout)

| Subagent | Role |
|---|---|
| Agent Router | Routes to specialist subagents |
| Rider Insights / Advisor Follow-up | Existing owners (Contacts) |
| Lead Engagement & Test Ride | Prospects (Leads) |
| General FAQ / Off Topic / Ambiguous Question | Platform defaults |

---

## 2. Phase 5 scope — what we are adding

Phase 5 extends Agentforce without unstructured RAG. All new **facts** stay on **Flows + DMOs**; **narrative** stays on **Data Library**.

```text
┌─────────────────────────────────────────────────────────────┐
│  SVT Advisor Copilot                                        │
├─────────────────────────────────────────────────────────────┤
│  Structured (existing + new Flows)                          │
│    • Lead context, intent, dealer, task                       │
│    • NEW: Unified prospect briefing                         │
│    • NEW: Service visit suggestion (rider)                  │
│    • NEW: Model specs lookup (optional CSV DMO)             │
├─────────────────────────────────────────────────────────────┤
│  Documents (Path A — existing)                              │
│    • Data Library: playbook, one-pagers, objections         │
│    • Answer Question with Knowledge                         │
├─────────────────────────────────────────────────────────────┤
│  Live data (existing)                                       │
│    • Ingestion API → intent bump (Karan MEDIUM → HIGH)      │
├─────────────────────────────────────────────────────────────┤
│  UI polish (optional)                                       │
│    • SVT Advisor Console Lightning page + agent panel       │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Build order (recommended)

| Sprint | Item | Effort | Demo value |
|---|---|---|---|
| **5a** | Finish Data Library + Lead subagent instructions | ~1 hr | Document citations |
| **5b** | Wire Data Library to Rider subagent | ~30 min | Cross-module talking points |
| **5c** | Unified prospect briefing Flow | ~2 hr | One-shot advisor prep |
| **5d** | Live Karan ingest rehearsal | ~1 hr | Real-time Data Cloud story |
| **5e** | Product catalog DMO + Get Model Specs Flow | ~3 hr | Deterministic specs |
| **5f** | SVT Advisor Console Lightning page | ~2 hr | Production-like UX |
| **5g** | Draft follow-up email Flow (optional) | ~2 hr | Human-in-the-loop gen |

Execute **5a → 5b → 5c → 5d** for the strongest demo with least work.

---

## 4. Build item 5a — Data Library (complete if not done)

**Reference:** [svt-data-library-org-setup.md](svt-data-library-org-setup.md)

### Checklist

- [ ] Data Library **`SVT Advisor Quick Guides`** — 4 PDFs indexed **Ready**
- [ ] Agent **Data → Data Library** → library selected
- [ ] **Answer Question with Knowledge** on Lead Engagement subagent
- [ ] Lead subagent instructions (Flows + document routing) pasted
- [ ] Stride 200 one-pager includes **Key Specs** (motor 4.2 kW, battery 3.2 kWh)
- [ ] Preview tests R1–R6 pass (see Data Library org setup doc)

---

## 5. Build item 5b — Rider subagent + Data Library

### Purpose

Let **Module 1** advisors get Stride 200 / Urban 125 talking points during retention calls without a separate agent.

### Steps

1. **Agent Builder → SVT Advisor Copilot**
2. Open subagent **Rider Insights** or **Advisor Follow-up** (your retention subagent name)
3. **Actions → Add → Answer Question with Knowledge**
4. Append to subagent instructions:

```text
DOCUMENT GROUNDING:
- Use existing rider Flow actions for profile, readiness, and follow-up tasks. Never infer readiness from PDFs.
- For product talking points, specs summaries, or objection scripts: use Answer Question with Knowledge (SVT Advisor Quick Guides).
- Cite document title. If not found: "I don't have that in the approved SVT documents."
```

5. **Save → Commit Version → Activate**

### Test prompts

| Prompt | Expected |
|---|---|
| Find ananya.rao@example.test and explain upgrade readiness. | Flow — readiness from DMO |
| What Stride 200 features should I mention for her upgrade call? | Data Library — A2 |
| Approve ₹20,000 discount for Ananya. | Refused |

---

## 6. Build item 5c — Unified prospect briefing Flow

### Purpose

One agent action returns everything an advisor needs before a call.

### Flow name

**`SVT Get Prospect Briefing`** (Autolaunched Flow)

### Inputs

| Input | Type | Source |
|---|---|---|
| `searchText` | Text | Advisor (email or name) |

### Logic (subflows or inline)

1. Call same elements as **Get Lead Context V2** → `leadId`, `leadName`, `prospectId`, `city`, `pinCode`, `contactPermission`, `hasOpenTestRideTask`, `openTaskSubject`
2. Call **Get Lead Intent v2** → `intentScore`, `preferredModel`, event summary fields if exposed
3. Call **Recommend Dealer** → `recommendedDealerName`, `matchType`, `primaryLanguage`
4. Assign output collection / structured text block for agent consumption

### Outputs

| Output | Description |
|---|---|
| `briefingStatus` | SUCCESS / NOT_FOUND / ERROR |
| `leadName` | Prospect name |
| `intentScore` | HIGH / MEDIUM / LOW |
| `preferredModel` | Model string |
| `recommendedDealerName` | Dealer |
| `matchType` | PIN or CITY |
| `contactPermission` | Boolean |
| `hasOpenTestRideTask` | Boolean |
| `openTaskSubject` | Text (if open task) |
| `briefingSummary` | Optional formula — one paragraph for agent display |

### Agent action

1. **Setup → Agent Assets → Actions → New**
2. Name: **`SVT Get Prospect Briefing`**
3. Link to Flow
4. Add to **Lead Engagement & Test Ride** subagent
5. Update instructions:

```text
When the advisor asks for a "briefing", "summary", or "everything before I call":
Run SVT Get Prospect Briefing once with searchText.
Present all returned fields. Do not run Get Lead Context, Get Intent, and Recommend Dealer separately unless the advisor asks a follow-up about one field only.
Do not offer to create a task unless contactPermission is true and hasOpenTestRideTask is false.
```

### Test prompts

| Prompt | Expected |
|---|---|
| Give me a full briefing on Naveen Kumar. | Single action; HIGH, Bengaluru, Stride 200, consent true |
| Briefing for priya.nair@example.test. | NOT_FOUND or ask for valid identifier |
| Briefing for Aditi Menon. | MEDIUM, Chennai, consent false noted |

### Acceptance criteria

- [ ] One action replaces three for briefing-style questions
- [ ] Intent/dealer/consent still from Flows, not PDFs
- [ ] Open task and consent flags surface correctly

---

## 7. Build item 5d — Live Karan ingest demo

**Reference:** [svt-realtime-ingestion-guide.md](svt-realtime-ingestion-guide.md) §6

### Demo script (5 minutes)

| Step | Action | Narration |
|---|---|---|
| 1 | *Karan Singh — intent and dealer?* | MEDIUM, Pune — static CSV data |
| 2 | POST `TestRideRequested` for `LEAD-2002` via PowerShell script | "Website form just fired an event" |
| 3 | Wait 3–5 min; verify Data Explorer → Website Engagement | Show new row |
| 4 | *What's Karan Singh's intent now?* | HIGH |
| 5 | *Stride 200 talking points for Karan* | Data Library A2 |
| 6 | Confirm → create test ride task | Flow + email |

### Prerequisites

- [ ] Ingestion API connector `SVT_Engagement_Events` active
- [ ] Data stream mapped to Website Engagement DMO
- [ ] ECA with `cdp_ingest_api`, `cdp_api`, `api`
- [ ] Script: [`docs/scripts/ingest-svt-engagement-event.ps1`](scripts/ingest-svt-engagement-event.ps1)

---

## 8. Build item 5e — Product catalog (structured specs)

### Purpose

Deterministic specs by model — complements Data Library narratives.

### Data file

Create `docs/svt-demo-data/svt_product_catalog.csv`:

```csv
model_name,battery_kwh,motor_peak_kw,range_km,charge_time_min,warranty_battery_years,warranty_vehicle_years,doc_version
SVT Stride 200 Demo,3.2,4.2,142,45,5,3,2026.1
SVT Urban 125 Demo,1.8,2.8,95,55,5,3,2026.1
```

### Data Cloud

1. **Data Streams → New → File Upload** (or update existing batch stream)
2. Map to DMO **`SVT Product Catalog`** (custom DMO or extend existing reference object)
3. Deploy stream

### Flow

**`SVT Get Model Specs`** — input `model` (Text) → lookup row → output spec fields.

### Agent action

Add to Lead Engagement (+ optional Rider subagent).

### Routing rule (instructions)

```text
For exact numeric specs (battery kWh, motor kW, range): use SVT Get Model Specs when model is known.
For advisor talking points and objection scripts: use Answer Question with Knowledge.
If values conflict, prefer SVT Get Model Specs for numbers and Data Library for narrative.
```

### Test prompts

| Prompt | Expected |
|---|---|
| What's the battery capacity for SVT Stride 200 Demo? | Flow: 3.2 kWh |
| What should I tell the customer about Stride 200 features? | Data Library: A2 |

---

## 9. Build item 5f — SVT Advisor Console (Lightning page)

### Purpose

Advisor workspace: profile + agent panel + readiness signals (Phase 5 polish from main demo guide).

### Page layout

| Region | Content |
|---|---|
| Header | Synthetic-data banner |
| Left column | Contact or Lead record detail |
| Right top | Upgrade readiness badge / intent badge (from report or formula — optional) |
| Right bottom | **Agentforce** conversation panel (embedded) |
| Related list | Tasks, Activities |

### Steps

1. **Setup → Lightning App Builder → New Page**
2. Template: **Header + Two Columns**
3. Add **Agentforce Agent** component (or Einstein Copilot panel — label varies by release)
4. Configure agent: **SVT Advisor Copilot**
5. Activate as org default for Sales App or custom **SVT Advisor** app
6. Assign to demo users

### Test

1. Open **Ananya Rao** Contact → page loads with agent panel
2. Open **Isha Sharma** Lead → same agent answers lead questions

---

## 10. Build item 5g — Draft follow-up email (optional)

### Purpose

Show generative assist **without** autonomous send.

### Flow

**`SVT Draft Follow-up Email`**

| Input | `leadId`, `purpose` (TestRide / Upgrade / Nurture) |
|---|---|
| Logic | Get Lead email + name + model; build template text in Flow (or Prompt Template if available) |
| Output | `draftSubject`, `draftBody`, `sendAllowed` (false always in v1) |

### Instructions

```text
When advisor asks to draft an email: run SVT Draft Follow-up Email.
Show draft for advisor review. Never send email from this action.
Customer email is sent only from SVT Create Lead Test Ride Task when appropriate.
```

---

## 11. Full demo script (15 minutes)

Combines all Phase 5 layers.

### Act 1 — Rider retention (3 min)

1. Open **Ananya Rao** on Advisor Console  
2. *Find ananya.rao@example.test — upgrade readiness and service context*  
3. *What Stride 200 points for the upgrade call?* → Data Library  
4. *Approve ₹20,000 discount* → refused  
5. *Create follow-up task* → confirm → created  

### Act 2 — Lead + documents (4 min)

6. *Full briefing on Naveen Kumar* → **SVT Get Prospect Briefing** (or three Flows)  
7. *Handle "too expensive" if he pushes back* → Objection Guide  
8. *Yes, create test ride task* → CREATED + emailSent  

### Act 3 — Live stream (4 min)

9. *Karan Singh — intent and dealer?* → MEDIUM  
10. Ingest `TestRideRequested` event  
11. *Karan's intent now?* → HIGH  
12. *Create test ride task for Karan* → confirm  

### Act 4 — Guardrails (2 min)

13. *Aditi Menon — create test ride task* → blocked (consent)  
14. *Priya Nair specs* → not found  

---

## 12. Master test matrix

| # | Prompt | Layer | Pass |
|---|---|---|---|
| T1 | Isha — intent and dealer | Flow | HIGH, Bengaluru |
| T2 | Full briefing Naveen | Briefing Flow | All fields |
| T3 | Stride 200 battery kWh | Specs Flow or Library | 3.2 |
| T4 | Motor peak power Stride 200 | Library (one-pager) | 4.2 kW |
| T5 | Test ride steps | Library | A1 cited |
| T6 | Too expensive objection | Library | A4, no ₹ |
| T7 | Karan live ingest → HIGH | Ingestion + Flow | Score changes |
| T8 | Aditi task create | Guardrail | Blocked |
| T9 | Discount approval | Guardrail | Refused |
| T10 | Ananya readiness | Flow only | Not from PDF |

---

## 13. Out of scope (do not build)

- S3 / UDLO / unstructured PDF ingest  
- Search Index / Retriever (Path B)  
- Autonomous customer email (except Create Task path)  
- Discount / financing approval  
- Real customer data  
- Production WhatsApp / telephony  

---

## 14. Success definition — Phase 5 complete

1. Data Library wired with citations on document questions.  
2. Flows handle all operational prospect/rider facts in same session.  
3. At least one **live ingest** demo (Karan) rehearsed.  
4. Optional: unified briefing Flow or Advisor Console page live.  
5. All guardrail tests (consent, duplicate task, discount) pass.  

---

## 15. Repo artifacts

| Path | Purpose |
|---|---|
| `docs/svt-agentforce-phase5-build.md` | This document |
| `docs/svt-data-library-org-setup.md` | Path A wiring |
| `docs/svt-rag-data-library/*.pdf` | Advisor PDFs |
| `docs/svt-demo-data/*.csv` | Structured demo sources |
| `docs/scripts/ingest-svt-engagement-event.ps1` | Live event POST |
| `docs/scripts/generate-svt-rag-pdfs.py` | Regenerate PDFs |

---

*Synthetic SVT Motors demo — not production guidance*
