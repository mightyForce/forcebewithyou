# How to Ingest More Prospects (Patients)

In this demo, **prospects = patients** modeled as Contacts at Summit Valley Medical Center, with Care Plans (Cases) and Tasks.

## Already seeded (8 patients total)

| Patient | Condition | Email |
|---------|-----------|-------|
| Maria Lopez | Type 2 Diabetes | maria.lopez.demo@summitvalley.health |
| James Chen | Cardiac recovery | james.chen.demo@summitvalley.health |
| Eleanor Whitmore | Senior wellness | eleanor.whitmore.demo@summitvalley.health |
| Robert Kim | COPD | robert.kim.demo@summitvalley.health |
| Sarah Patel | Prenatal care | sarah.patel.demo@summitvalley.health |
| David Morrison | Mental health | david.morrison.demo@summitvalley.health |
| Linda Foster | Oncology survivorship | linda.foster.demo@summitvalley.health |
| Carlos Rivera | Asthma | carlos.rivera.demo@summitvalley.health |

---

## Method 1: Salesforce UI (single prospect)

1. **Contacts** → New
2. Link to **Summit Valley Medical Center** (`001gL00001jyf99QAA` in Agentforce org)
3. Use email pattern: `firstname.lastname.demo@summitvalley.health`
4. On the Contact → **New Case** → Subject: `Care Plan — {Program} ({Name})`
5. On the Contact → **New Task** for each care activity

---

## Method 2: Data Import Wizard (bulk — Contacts only)

1. **Setup** → **Data Import Wizard**
2. Choose **Contacts** → **Accounts and Contacts**
3. Upload `demo/prospects-template.csv` (Contacts columns only: FirstName, LastName, Email, Phone, Birthdate, Title, AccountId, Description)
4. Map fields → Start Import

Then create Cases and Tasks manually or via Method 3/4.

---

## Method 3: Data Loader (bulk — all objects)

Use **Salesforce Data Loader** or **sf CLI**:

### Step 1 — Insert Contacts

CSV columns: `FirstName,LastName,Email,Phone,Birthdate,Title,AccountId,Description`

### Step 2 — Insert Cases (care plans)

CSV columns: `Subject,Status,Priority,Description,ContactId,AccountId,Origin`

- `ContactId` = ID from Step 1
- `AccountId` = `001gL00001jyf99QAA` (Summit Valley)
- `Origin` = `Phone`
- `Status` = `Working`

### Step 3 — Insert Tasks

CSV columns: `Subject,Status,Priority,Description,WhoId`

- `WhoId` = Contact ID from Step 1

---

## Method 4: Salesforce CLI (scriptable)

```bash
# Insert a contact
sf data create record --sobject Contact \
  --values "FirstName='Jane' LastName='Doe' Email='jane.doe.demo@summitvalley.health' AccountId='001gL00001jyf99QAA' Birthdate=1980-01-15 Title='Patient'" \
  --target-org your-org-alias

# Insert care plan (replace CONTACT_ID)
sf data create record --sobject Case \
  --values "Subject='Care Plan — Weight Management (Jane Doe)' Status='Working' Priority='Medium' ContactId='CONTACT_ID' AccountId='001gL00001jyf99QAA' Origin='Phone'" \
  --target-org your-org-alias

# Insert task (replace CONTACT_ID)
sf data create record --sobject Task \
  --values "Subject='Nutrition counseling' Status='Not Started' Priority='Normal' WhoId='CONTACT_ID'" \
  --target-org your-org-alias
```

---

## Method 5: REST API / Apex (OmniStudio Integration Procedure)

For production Health Cloud ingestion:

1. Build an **Integration Procedure** that accepts a JSON array of prospects
2. Use **Data Mapper Load** to upsert Contacts (patients)
3. Chain IP actions to create Care Plans and Tasks
4. Trigger from OmniScript, Flow, or external API

Template JSON structure: see `demo/prospects-batch.json`.

---

## Method 6: Add rows to CSV template

To add 5 more prospects yourself:

1. Copy a row in `demo/prospects-template.csv`
2. Change name, email, condition, care plan subject, tasks
3. Import via Data Loader (Contacts first, then Cases, then Tasks)

---

## Verify ingestion

```sql
SELECT Id, FirstName, LastName, Email
FROM Contact
WHERE Email LIKE '%summitvalley.health'
ORDER BY LastName

SELECT Id, Subject, Status, Contact.FirstName, Contact.LastName
FROM Case
WHERE Subject LIKE 'Care Plan%'
ORDER BY Contact.LastName

SELECT Id, Subject, Status, Who.Name
FROM Task
WHERE Who.Email LIKE '%summitvalley.health'
ORDER BY Who.Name
```

---

## Native Health Cloud (when licensed)

Replace this mapping with:

| Demo | Health Cloud |
|------|--------------|
| Contact | Person Account (Patient) |
| Case | CarePlan |
| Task | CarePlanGoal / Activity |

Use **Health Cloud data models** and **Care Plan Templates** for production ingestion.
