# SVT demo — Agentforce Data Library org setup (Path A)

Step-by-step guide to wire **SVT Advisor Quick Guides** into **SVT Advisor Copilot** in your Salesforce org.

**Prerequisite:** Phases 1–3 built (Flows, agent, subagents). See [main demo guide](svt-data-cloud-agentforce-demo.md).

**Reference:** [Document grounding pilot v1.1](svt-rag-pilot-v1-reference.md)

---

## What you are building

```text
4 advisor PDFs
  → Agentforce Data Library (SVT Advisor Quick Guides)
  → Agent-level Data Library (Data → Data Library)
  → Lead Engagement subagent uses Answer Question with Knowledge + Flow routing via instructions
  → agent cites documents for specs / playbook / objections
  → Flows still handle intent, dealer, consent, tasks
```

**Time:** ~30–45 minutes (plus 10–15 min for library indexing after upload)

---

## Step 1 — Get the PDFs

Download all four files from the repo folder [`docs/svt-rag-data-library/`](svt-rag-data-library/):

| Upload order | File |
|---|---|
| 1 | `SVT_Advisor_Test_Ride_Playbook.pdf` |
| 2 | `SVT_Stride_200_Advisor_OnePager.pdf` |
| 3 | `SVT_Urban_125_Advisor_OnePager.pdf` |
| 4 | `SVT_Objection_Handling_Guide.pdf` |

Regenerate locally if needed:

```bash
pip install fpdf2
python3 docs/scripts/generate-svt-rag-pdfs.py
```

---

## Step 2 — Create the Data Library

1. Open **Setup** (gear icon).
2. Quick Find: **`Data Library`** or **`Agentforce Data Library`**.
   - Path is often: **Setup → Agentforce → Data Library**
   - Some orgs: **Setup → Einstein → Agentforce Data Library**
3. Click **New** (or **New Data Library**).
4. Fill in:

| Field | Value |
|---|---|
| **Name** | `SVT Advisor Quick Guides` |
| **Description** | Synthetic SVT Motors advisor guides — test ride playbook, model one-pagers, objection handling. Demo only. |

5. Click **Save**.
6. On the library detail page, click **Add Files** or **Upload**.
7. Upload all **4 PDFs** (multi-select if supported).
8. Wait until each file shows status **Ready** / **Indexed** (can take 5–15 minutes).
   - Refresh the page if status stays “Processing”.
   - Do not attach to the agent until all files are ready.

**Tip:** If upload fails, try one PDF at a time. Max file size varies by org; these demo PDFs are small (~2 KB each).

---

## Step 3 — Attach library to the agent (agent-level, not per subagent)

In **Agent Builder** (Agent Authoring), the Data Library is configured at the **agent** level under **Data → Data Library** — it is **not** nested inside a subagent. Your screenshot setup is correct.

1. Open **Agent Builder → SVT Advisor Copilot**.
2. In the left outline, under **Data**, click **Data Library** (sibling to **Subagents**, not inside one).
3. Select **`SVT Advisor Quick Guides`** from the dropdown.
4. Optional: check **Show sources** if you want citations visible in the UI during Live Test.
5. Click **Save** (top right).

Salesforce wires this through the built-in **Answer Question with Knowledge** action, which searches the library and grounds responses.

> **Note:** All subagents on this agent can *access* the library, but **instructions** control *when* each subagent should use Flows vs knowledge. Put document routing rules on **Lead Engagement & Test Ride** (and optionally **Rider Insights**).

### Ensure knowledge action is available

1. Open subagent **Lead Engagement & Test Ride**.
2. Under **Actions** (or **Actions Available for Reasoning**), confirm **Answer Question with Knowledge** is present.
   - If missing: **Add action → Standard / Knowledge → Answer Question with Knowledge**.
3. Keep your four SVT Flow actions on the same subagent.

Repeat for **Rider Insights / Advisor Follow-up** only if you want document answers in Module 1.

---

## Step 4 — Update subagent instructions

Open **`Lead Engagement & Test Ride`** → **Instructions** (or **System Instructions**).

**Replace or merge** with the block below. Keep your existing Flow action names if they differ slightly.

```text
You help dealer sales advisors qualify prospects, score intent, recommend dealers, and schedule test rides for SVT Motors (fictional demo).

ACTION ORDER (operational questions — always use Flows, never PDFs):
1. SVT Get Lead Context — when a prospect is mentioned (email or name as searchText).
2. SVT Get Lead Intent — pass prospectId from step 1.
3. SVT Recommend Dealer — pass city, pinCode, and model from step 1.
4. SVT Create Lead Test Ride Task — only after explicit advisor confirmation; pass userConfirmed=true only after yes.

OPERATIONAL RULES:
- Never ask the advisor for a Salesforce Lead Id (00Q...).
- If contactPermission is false: still report intent and dealer; do NOT offer or create a test-ride task.
- Require explicit confirmation before creating any test-ride task.
- Check hasOpenTestRideTask if available; do not create duplicate open test-ride tasks.
- When a task is created with consent, report emailSent status from the Flow.

DOCUMENT GROUNDING (SVT Advisor Quick Guides — agent-level Data Library):
- The agent has Data Library "SVT Advisor Quick Guides" attached. Use the Answer Question with Knowledge action for document lookups.
- Use Flow actions for intent, dealer, consent, and task creation. NEVER infer these from PDFs.
- Use the Data Library for: test ride process, model talking points, key specs on one-pagers, objection handling scripts.
- Always cite the document title (e.g. "According to SVT Stride 200 Demo - Advisor One-Pager...").
- If the answer is not in retrieved documents, say: "I don't have that in the approved SVT documents."
- Do not invent specs, warranty terms, or pricing not stated in retrieved documents.

GUARDRAILS:
- Do not approve discounts, financing, warranty claims, refunds, or payments.
- Do not quote on-road prices or rupee amounts unless explicitly in a retrieved document — and still never approve discounts.
- All prospect names and data are synthetic demo data.
```

8. **Save** subagent → **Save** agent.

---

## Step 5 — Activate the agent

1. In Agent Builder, click **Activate** (or **Publish**).
2. Confirm the runtime user has access to:
   - All four lead Flow actions
   - Data Library / knowledge grounding entitlement
3. Open **Live Test** or the **Sales App** agent panel to test.

If activation fails on library access, assign the admin/runtime user **Agentforce** and **Einstein** permissions that include Data Library.

---

## Step 6 — Test (run in order)

Wait until Data Library files show **Ready** before testing document prompts.

### A. Flows still work (no PDF)

| # | Prompt | Expected |
|---|---|---|
| 1 | Isha Sharma is interested in a test ride — what's her intent and which dealer should we use? | HIGH, SVT Bengaluru Central (Flow) |
| 2 | Aditi Menon wants a test ride — what's her intent and which dealer? | MEDIUM, Chennai; consent warning; no task offer |

### B. Data Library cites documents

| # | Prompt | Expected |
|---|---|---|
| 3 | What are the test ride steps for Naveen Kumar? | Cites **Test Ride Playbook** — license, helmet, 15-min route |
| 4 | What should I highlight about the SVT Stride 200 Demo for Naveen? | Cites **Stride 200 One-Pager** — 3.2 kWh, features |
| 5 | What's the Stride 200 battery capacity per our advisor guide? | **3.2 kWh** from one-pager |
| 6 | How should I handle a "too expensive" objection? | Cites **Objection Handling Guide**; no ₹ amounts |

### C. Combined Flow + document (best demo moment)

| # | Prompt | Expected |
|---|---|---|
| 7 | Naveen Kumar — what's his intent and dealer? | Flow: HIGH, SVT Bengaluru Central |
| 8 | Give me Stride 200 talking points for his call | Data Library: A2 bullets |
| 9 | Yes, create the test ride task | Flow: Task created, emailSent if consent |

### D. Guardrails

| # | Prompt | Expected |
|---|---|---|
| 10 | Approve a 15% discount based on the objection guide | **Refused** — escalate to manager |
| 11 | What are Priya Nair's specs? | Not found / no fabrication |

---

## Step 7 — Demo narration (30 seconds)

> “Operational data — intent, dealer, consent — comes from Data Cloud through governed Flow actions. Advisor guides and product talking points come from our Data Library. The copilot cites the document; it doesn't invent specs or approve discounts.”

---

## Troubleshooting

| Issue | Fix |
|---|---|
| Data Library option missing in Setup | Enable Agentforce / Einstein; check org has Data Library entitlement |
| Files stuck on Processing | Wait 15 min; re-upload one PDF; check file is valid PDF |
| Agent doesn't cite documents | Confirm **Data → Data Library** has SVT Advisor Quick Guides; files Ready; **Answer Question with Knowledge** on subagent |
| Agent uses PDF for intent/dealer | Strengthen instructions: “NEVER infer intent from PDFs”; test prompt 1 again |
| Invented specs (wrong kWh) | Re-test after indexing complete; verify A2 uploaded |
| Flow works but document questions fail | Library not attached or still indexing |
| Document works but Flow fails | Unrelated — check Flow actions still on subagent |

---

## Checklist

- [ ] 4 PDFs uploaded; all **Ready**
- [ ] Library **`SVT Advisor Quick Guides`** created
- [ ] Library **`SVT Advisor Quick Guides`** selected under agent **Data → Data Library**
- [ ] **Answer Question with Knowledge** on Lead Engagement subagent
- [ ] Instructions updated (Flows + document routing)
- [ ] Agent **Activated**
- [ ] Tests 1–2 pass (Flows)
- [ ] Tests 3–6 pass (citations)
- [ ] Test 10 passes (discount refused)

---

## Related docs

- [Pilot reference v1.1](svt-rag-pilot-v1-reference.md)
- [Main demo guide](svt-data-cloud-agentforce-demo.md)
- [Real-time ingestion](svt-realtime-ingestion-guide.md) — structured streaming (separate from Data Library)

---

*Synthetic SVT Motors demo — not production guidance*
