# Health Cloud Demo Walkthrough

## Overview

This demo illustrates core Salesforce Health Cloud concepts — patient-centric care coordination, care plans, goals, and task assignment — using standard Salesforce objects in an org without Health Cloud licensing.

## Demo Actors

### Organizations

| Account | Type | Role |
|---------|------|------|
| Summit Valley Medical Center | Healthcare Provider | Primary care and specialty services |
| BlueCross Regional Health Plan | Payer | Regional health insurance |

### Patients

| Patient | Age | Condition | Care Plan |
|---------|-----|-----------|-----------|
| Maria Lopez | 61 | Type 2 Diabetes (HbA1c 8.2%) | Diabetes Management |
| James Chen | 48 | Post-cardiac surgery recovery | Cardiac Recovery |
| Eleanor Whitmore | 77 | Hypertension, mobility limitations | Senior Wellness |

## Demo Script (15 minutes)

### Act 1: Patient 360 View (3 min)

1. Navigate to **Contacts** and search for `Maria Lopez`.
2. Review patient demographics: birthdate, email, phone, linked provider account.
3. In a full Health Cloud org, this would be a **Person Account** with a Patient 360 timeline showing clinical events, medications, and care team members.

**Talking point:** Health Cloud unifies clinical and non-clinical data into a single patient view, eliminating context-switching between systems.

### Act 2: Care Plan Review (5 min)

1. From Maria Lopez's contact record, open the related **Cases**.
2. Open **Care Plan — Diabetes Management**.
3. Read the Description field — it contains the structured care plan:
   - **Problem:** Type 2 Diabetes with HbA1c 8.2%
   - **Goal:** Reduce HbA1c below 7% within 90 days
   - **Interventions:** Nutrition counseling, medication adherence, glucose monitoring

4. Repeat for James Chen (Cardiac Recovery) and Eleanor Whitmore (Senior Wellness).

**Talking point:** In Health Cloud, care plans use native objects (`CarePlan`, `CarePlanGoal`, `CarePlanGoalTarget`) with templates, status tracking, and automated task generation.

### Act 3: Care Activities & Task Management (5 min)

1. Navigate to **Tasks** and filter by patient name.
2. Review Maria's tasks:
   - Schedule HbA1c lab test (Not Started, High priority)
   - Nutrition counseling referral (In Progress)
   - Daily glucose monitoring (In Progress)
3. Update a task status to demonstrate workflow progression.

**Talking point:** Tasks can be assigned to patients, caregivers, or care team members. Health Cloud supports patient-facing portals where patients complete assigned activities.

### Act 4: Care Coordination Query (2 min)

Run this query in Developer Console to see all active care plans with patient details:

```sql
SELECT Id, Subject, Status, Priority,
       Contact.FirstName, Contact.LastName,
       Contact.Email, Account.Name
FROM Case
WHERE Subject LIKE 'Care Plan%'
ORDER BY Priority DESC, Contact.LastName
```

**Talking point:** Health Cloud adds pre-built dashboards, care gap analytics, and risk scoring on top of this data model.

## Health Cloud Native Features (Upgrade Path)

When Health Cloud is licensed, the demo maps to these native capabilities:

| Capability | Health Cloud Feature |
|------------|---------------------|
| Patient records | Person Accounts with Health Cloud patient fields |
| Care plans | CarePlan, CarePlanTemplate, CarePlanGoal objects |
| Clinical data | ClinicalEncounter, MedicationRequest, DiagnosticReport |
| Care teams | CareTeamMember with role-based access |
| Risk scoring | Intelligent care gap identification |
| Patient engagement | Experience Cloud patient portal |
| Utilization management | MemberPlan, CoverageBenefit for payers |
| Provider network | HealthcareProvider, HealthcareFacility |

### Trailhead Resources

- [Health Cloud: Care Plans](https://trailhead.salesforce.com/content/learn/modules/health-cloud-care-plans)
- [Health Cloud Basics](https://trailhead.salesforce.com/content/learn/modules/health-cloud-basics)

## Record IDs (Demo Data Reference)

See `demo/seed-data.json` for all seeded record IDs in your org.
