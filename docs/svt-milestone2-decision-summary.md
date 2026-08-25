# SVT Milestone 2 — Decision summary

**Date:** August 2026  
**Status:** Architecture frozen — ready to build in org  
**Scope:** CRM Vehicle layer + Advisor Console foundation  

---

## Executive summary

We are adding a **`Vehicle__c`** custom object on CRM for the **rider / advisor path**, separate from the existing **lead / Agentforce path**. Dealer on Vehicle uses **Lookup → Account**. Model uses a **12-value SKU picklist** aligned with `svt_product_catalog.csv`.

**This milestone does not change** any existing Agentforce Flows, lead subagent instructions, actions, or Data Cloud data streams.

---

## Frozen decisions

| # | Decision | Choice |
|---|---|---|
| 1 | `Vehicle__c.Preferred_Dealer__c` | **Lookup → Account** (not text) |
| 2 | `Vehicle__c.Model_SKU__c` | **Picklist — 12 SKUs** from product catalog |
| 3 | Salesforce Product / catalog object | **No** — catalog stays in Data Cloud for now |
| 4 | `vehicle_service_history.csv` (Data Cloud) | **Unchanged** — `preferred_dealer` stays text |
| 5 | Recommend Dealer Flow | **Do not modify** |
| 6 | Create Lead Test Ride Task Flow | **Do not modify** |
| 7 | Lead agent / subagent instructions | **Do not modify** |
| 8 | `Service_Visit__c` | **Defer** until Contact → Vehicle → Console works |
| 9 | Advisor Console LWC | **No changes** until vehicle data is loaded (Step 2D) |

---

## Two-path architecture

### Path A — Lead / Agentforce (unchanged)

```text
Data Cloud
  prospects.csv
  dealer_directory.csv (SVT Dealer Directory DMO)
  lead_intent_events.csv
        ↓
  SVT Get Lead Context V2
  SVT Get Lead Intent v2
  SVT Recommend Dealer          → recommendedDealerName (TEXT)
  SVT Create Lead Test Ride Task → dealerName (TEXT)
        ↓
  Lead Engagement subagent
  SVT Advisor Copilot
```

### Path B — Rider / Advisor Console (new)

```text
Contact (Primary Rider)
        ↓
  Vehicle__c
    ├── Vehicle_Number__c
    ├── VIN__c
    ├── Model_SKU__c              (12 SKU picklist)
    ├── Odometer__c
    ├── Warranty_End_Date__c
    ├── Last_Service_Date__c
    ├── Last_Service_Odometer_km__c
    └── Preferred_Dealer__c  →  Account (dealer)
                                      ↓
                              SVT Advisor Console (LWC — Step 2D)
```

**Product master:** `svt_product_catalog.csv` (Data Cloud) defines the 12 SKUs. No separate Salesforce Product object for this demo.

---

## Impact on agents, actions, instructions, and Flows

| Component | Impact during Milestone 2 |
|---|---|
| SVT Advisor Copilot / subagents | **None** |
| Lead Engagement instructions | **None** |
| SVT Get Lead Context V2 | **None** |
| SVT Get Lead Intent v2 | **None** |
| SVT Recommend Dealer | **None** — still uses Data Cloud DMO |
| SVT Create Lead Test Ride Task | **None** — still uses text `dealerName` |
| Rider retention agent (current) | **None** — reads Data Cloud, not Vehicle yet |
| Answer Question with Knowledge | **None** |
| Streaming Ingestion API | **None** |
| Data Cloud streams | **None** |

### Simple rule

```text
Lead / prospect questions  →  existing Flows + Data Cloud (unchanged)
Owned vehicle / console    →  new Vehicle__c + Account lookup (new, separate)
```

Impact occurs **only if you later** wire Vehicle into agent Flows or change Recommend Dealer to use CRM Accounts. That is **out of scope** for Milestone 2.

---

## Vehicle__c field list (frozen)

| Field label | API name | Type |
|---|---|---|
| Vehicle Number | `Vehicle_Number__c` | Text, External ID, Unique, Required |
| VIN | `VIN__c` | Text, Unique, Required |
| Primary Rider | `Primary_Rider__c` | Lookup → Contact, Required |
| Model SKU | `Model_SKU__c` | Picklist (12 values), Required |
| Purchase Date | `Purchase_Date__c` | Date |
| Registration Date | `Registration_Date__c` | Date |
| Odometer | `Odometer__c` | Number(12,0) |
| Status | `Status__c` | Picklist: Active, Inactive, Sold, Traded In (default Active) |
| Warranty End Date | `Warranty_End_Date__c` | Date |
| Preferred Dealer | `Preferred_Dealer__c` | Lookup → Account |
| Last Service Date | `Last_Service_Date__c` | Date |
| Last Service Odometer | `Last_Service_Odometer_km__c` | Number(12,0) |
| Registration Number | `Registration_Number__c` | Text (optional) |
| Demo Data | `Demo_Data__c` | Checkbox (default true) |

### Model_SKU__c — 12 picklist values

```text
SVT Stride 200 Demo
SVT Stride 200 Pro
SVT Urban 125 Demo
SVT Urban 125 Plus
SVT Pulse 160 Standard
SVT Pulse 160 Long Range
SVT Nova 110 Lite
SVT Nova 110 Connect
SVT Apex 300 Sport
SVT Apex 300 Tour
SVT Glide 90 Eco
SVT Glide 90 Family
```

Source: `docs/svt-demo-data/svt_product_catalog.csv`

---

## Milestone 2 build sequence

| Step | Name | What to do |
|---|---|---|
| **2A** | Dealer CRM foundation | Create `Dealer_ID__c` on Account; import 7 dealer Accounts |
| **2B** | Vehicle CRM foundation | Create `Vehicle__c` with fields above; add related list on Contact |
| **2C** | Vehicle data load | Import 6 vehicles; link to Contacts and dealer Accounts |
| **2D** | Dynamic LWC | Replace hardcoded vehicle fields with live `Vehicle__c` data |

**Agentforce / copilot integration comes after 2D is verified.**

---

## Step 2A — Dealer Accounts

1. Add on **Account**: **`Dealer_ID__c`** (Text, External ID, Unique)
2. Import **`svt_dealer_accounts_import.csv`**

| Dealer_ID__c | Account Name |
|---|---|
| DLR-4001 | SVT Bengaluru Central |
| DLR-4002 | SVT Pune West |
| DLR-4003 | SVT Chennai North |
| DLR-4004 | SVT Delhi South |
| DLR-4005 | SVT Ahmedabad One |
| DLR-4006 | SVT Kochi Central |
| DLR-4007 | SVT Hyderabad Central |

Names must match `dealer_name` in `dealer_directory.csv` (Data Cloud).

---

## Step 2C — Six demo vehicles

Source: `vehicle_service_history.csv` → CRM import via **`svt_vehicles_crm_import.csv`**

| Contact email | Vehicle Number | Model SKU | Dealer ID |
|---|---|---|---|
| ananya.rao@example.test | SVT-VEH-2001 | SVT Stride 200 Demo | DLR-4001 |
| vikram.mehta@example.test | SVT-VEH-2002 | SVT Stride 200 Pro | DLR-4002 |
| meera.iyer@example.test | SVT-VEH-2003 | SVT Urban 125 Demo | DLR-4003 |
| arjun.kapoor@example.test | SVT-VEH-2004 | SVT Pulse 160 Standard | DLR-4004 |
| nisha.patel@example.test | SVT-VEH-2005 | SVT Nova 110 Lite | DLR-4005 |
| rahul.nair@example.test | SVT-VEH-2006 | SVT Apex 300 Sport | DLR-4006 |

**Prerequisites:** 6 rider Contacts exist; 7 dealer Accounts imported.

**Verify:** Open Ananya Rao → Vehicles related list → odometer **10400**, dealer **SVT Bengaluru Central**.

---

## Explicit do-not-touch list

Do **not** modify during Milestone 2 (Steps 2A–2C):

- SVT Get Lead Context V2  
- SVT Get Lead Intent v2  
- SVT Recommend Dealer  
- SVT Create Lead Test Ride Task  
- Lead Engagement & Test Ride subagent instructions  
- Any Data Cloud data stream or CSV re-upload (except new optional product catalog stream)  
- Streaming Ingestion API connector / ECA  
- Agentforce Data Library (Path A)  
- Advisor Console LWC (until Step 2D)  

---

## Repo reference files

| File | Purpose |
|---|---|
| [`svt-milestone2-advisor-workspace.md`](svt-milestone2-advisor-workspace.md) | Detailed build guide |
| [`svt-milestone2-decision-summary.md`](svt-milestone2-decision-summary.md) | This document |
| [`svt-demo-data/svt_dealer_accounts_import.csv`](svt-demo-data/svt_dealer_accounts_import.csv) | 7 dealer Accounts |
| [`svt-demo-data/svt_vehicles_crm_import.csv`](svt-demo-data/svt_vehicles_crm_import.csv) | 6 vehicles for CRM load |
| [`svt-demo-data/svt_product_catalog.csv`](svt-demo-data/svt_product_catalog.csv) | 12 SKU master (Data Cloud + picklist source) |
| [`svt-demo-data/vehicle_service_history.csv`](svt-demo-data/vehicle_service_history.csv) | Data Cloud snapshot — **do not change** |
| [`svt-vehicle-product-catalog-setup.md`](svt-vehicle-product-catalog-setup.md) | Catalog usage options |

---

## Build prompt guardrail (copy-paste)

```text
Milestone 2 only: Create Account.Dealer_ID__c, Vehicle__c, import 7 dealer
Accounts and 6 vehicles from repo CSVs. Do NOT modify Agentforce Flows, lead
subagent instructions, Data Cloud streams, or Advisor Console LWC until
vehicle load is verified (Step 2C).
```

---

## Deferred (post Milestone 2)

| Item | When |
|---|---|
| `Service_Visit__c` object | After Contact → Vehicle → Console works |
| Wire Vehicle into rider agent / Flows | Optional — after 2D |
| Unify Recommend Dealer with CRM Accounts | Optional — Phase 3+ |
| Data Cloud product catalog stream | Optional — for agent spec lookup Flow |

---

*Synthetic SVT Motors demo — not production guidance*
