# SVT demo — test ride confirmation email (Option B)

Send a consent-gated confirmation email to the prospect when **SVT Create Lead Test Ride Task** successfully creates a Task.

Related: [SVT Motors Data Cloud + Agentforce demo](svt-data-cloud-agentforce-demo.md)

---

## Architecture

```text
Create Lead Test Ride Task
  → userConfirmed? consent? no open task?
  → Create Task (CREATED)
  → Get Lead (email, first name)
  → contactPermission = true AND email not blank?
      Yes → Send Email (template)
      No  → skip
  → Assign message (include email sent or skipped)
```

Email runs **only** when:

- Task was **CREATED** (not `ALREADY_EXISTS`)
- `contactPermission` is **true**
- Lead has a valid **Email**

---

## Step 1 — Deliverability (demo org)

1. **Setup → Deliverability**
2. Set **Access Level** to **All email** (required for Dev Edition demos)

---

## Step 2 — Org-Wide Email Address (recommended)

1. **Setup → Organization-Wide Addresses → Add**
2. Display Name: `SVT Motors`
3. Email: use a verified address (your user email is fine for demo)
4. Allow all profiles to use this address
5. Verify via inbox link

Note the **Org-Wide Email Address Id** if the Send Email action asks for it.

---

## Step 3 — Email template

1. **Setup → Classic Email Templates → New Template**
2. Folder: **Public Email Templates** (or SVT demo folder)
3. **HTML (using Classic Letterhead)** or **Custom (without letterhead)** — either works for demo
4. **Available For Use:** checked
5. **Related Entity Type:** Lead

**Template name:** `SVT Test Ride Confirmation`

**Subject:**

```text
Your SVT test ride request – {!Lead.FirstName}
```

**Body (HTML or plain text):**

```text
Hi {!Lead.FirstName},

Thank you for your interest in the SVT Stride 200 Demo.

We've received your test ride request for the {!relatedTo.model} at {!relatedTo.dealerName}.

Our team at the dealership will contact you shortly to confirm your preferred date and time.

If you did not request this, please ignore this email.

— SVT Motors
Demo only. Synthetic data.
```

> **Note:** `{!relatedTo.field}` merge syntax works when the Send Email action passes **Related Record Id** = `{!leadId}` and the template is Lead-based. If merge fields for `model` / `dealerName` do not resolve (they are Flow variables, not Lead fields), use the **Simplified body** below instead and pass values via a **Text Template** in Flow (see Step 5 alternate).

### Simplified template (Lead fields only)

**Subject:** `Your SVT test ride request`

**Body:**

```text
Hi {!Lead.FirstName},

Thank you for your interest in SVT Motors.

We've received your test ride request. A dealership advisor will contact you shortly at {!Lead.Email} to confirm date and time.

— SVT Motors
```

Use Flow to append dealer/model in the Send Email **Description** or use a **Text Template** resource (recommended — see Step 5).

---

## Step 4 — Text Template in Flow (recommended for model + dealer)

In **SVT Create Lead Test Ride Task**, create a **Text Template** resource:

**API Name:** `emailBodyTemplate`

**Body:**

```text
Hi {!Get_Lead.FirstName},

Thank you for your interest in SVT Motors.

We've received your test ride request for the {!model} at {!dealerName}.

Our team will contact you shortly at {!Get_Lead.Email} to confirm your preferred date and time.

— SVT Motors
(Demo — synthetic data)
```

Use this with the **Send Email** action's body field if your org supports free-form body; otherwise use Classic template with Lead-only merges and mention model/dealer in the Task Description only.

---

## Step 5 — Update **SVT Create Lead Test Ride Task** flow

### New / confirm variables

| API Name | Type | Direction | Notes |
|---|---|---|---|
| `emailSent` | Boolean | Output | true if email action ran |
| `message` | Text | Output | existing — extend text |
| `contactPermission` | Boolean | Input or internal | must already exist from consent check |

Add input **`contactPermission`** (Boolean) if the flow does not already resolve it internally — the agent passes it from **Get Lead Context**.

Update **Agent Action** inputs to include `contactPermission` if not already wired.

### Flow path (after successful Create Task)

Insert **after** Create Test Ride Task, **before** final CREATED assignment:

```text
Create Test Ride Task
  ↓
Get Records: Get Lead
  Object: Lead
  Filter: Id Equals {!leadId}
  Store: First record, all fields
  ↓
Decision: Send Confirmation Email?
```

**Outcome: Send Email** — All conditions met (AND):

| Condition | Value |
|---|---|
| `{!contactPermission}` | Equals `{!$GlobalConstant.True}` |
| `{!Get_Lead.Email}` | Is Null | **False** (email exists) |

**Default: Skip Email**

### Send Email action (Send Email branch)

1. **+ → Action → Send Email**
2. Configure (labels vary slightly by release):

| Field | Value |
|---|---|
| **Related Record Id** | `{!leadId}` |
| **Recipient Id** | `{!leadId}` |
| **Email Template Id** | `SVT Test Ride Confirmation` |
| **Log Email on Send** | true (recommended — shows on Lead Activity) |

If using **Text Template** instead of Classic template:

| Field | Value |
|---|---|
| **To** | `{!Get_Lead.Email}` |
| **Subject** | `Your SVT test ride request – {!Get_Lead.FirstName}` |
| **Body** | `{!emailBodyTemplate}` |
| **Related To** | `{!leadId}` |

3. **Fault path:** connect to Assignment **Email Failed** (optional) — still return CREATED for task; set `emailSent = false` and note in message.

### Assignments

**After Send Email (success branch):**

| Variable | Value |
|---|---|
| `{!emailSent}` | true |
| `{!taskStatus}` | CREATED |
| `{!message}` | `Test ride task created and assigned to you. Confirmation email sent to {!Get_Lead.Email}.` |

**Skip Email branch:**

| Variable | Value |
|---|---|
| `{!emailSent}` | false |
| `{!taskStatus}` | CREATED |
| `{!message}` | `Test ride task created and assigned to you. No confirmation email sent (consent or email missing).` |

**ALREADY_EXISTS / BLOCKED branches:** unchanged — no email.

---

## Step 6 — Update Agent Action

**Setup → Agent Assets → Actions → SVT Create Lead Test Ride Task**

1. Add input **`contactPermission`** (Boolean) if new
2. Add output **`emailSent`** (Boolean) — optional but useful for subagent
3. Save and refresh action on subagent

**Agent passes on create:**

| Input | Source |
|---|---|
| `leadId` | Get Lead Context |
| `dealerName` | Recommend Dealer |
| `model` | Get Lead Intent |
| `userConfirmed` | true after advisor confirms |
| `contactPermission` | Get Lead Context |

---

## Step 7 — Subagent instruction add

Add under the CREATED block:

```text
If SVT Create Lead Test Ride Task returns taskStatus CREATED:
- If emailSent is true, tell the advisor the task was created AND a confirmation email was sent to the prospect.
- If emailSent is false, tell the advisor the task was created but no email was sent (consent or missing email).
- Do not create again for the same lead in this session.
```

---

## Step 8 — Test

### Flow debug

| Input | Expected |
|---|---|
| leadId = Isha, userConfirmed = true, contactPermission = true | CREATED, emailSent = true |
| leadId = Aditi, contactPermission = false | BLOCKED_CONSENT — no task, no email |
| leadId with no email | CREATED, emailSent = false |

### Live test

1. Use a **real email you control** on a test Lead (e.g. your inbox)
2. Ask agent to create task for that lead
3. Check **Lead → Activity → Email** and your inbox

### Deliverability troubleshooting

| Issue | Fix |
|---|---|
| Email not received | Setup → Deliverability → All email |
| Send Email action greyed out | Enable Email Administration permission; check flow type |
| Template merge blank | Use Text Template with Flow variables |
| Bounce | Use verified org-wide address |

---

## Security and demo notes

- Email sends **only** when `contactPermission = true` (same guardrail as task creation)
- Aditi / Sneha never receive email
- Log email on Lead for audit trail
- Regenerate demo credentials after sharing screenshots
