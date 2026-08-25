# Milestone 2 — SVT Advisor Workspace (CRM Vehicle layer)

**Status:** Frozen architecture — ready to build in org  
**Out of scope for this milestone:** Agent Flows, Data Cloud streams, lead agent, Service_Visit__c, LWC changes

---

## Frozen decisions

| Decision | Choice |
|---|---|
| `Vehicle__c.Preferred_Dealer__c` | **Lookup → Account** |
| `Vehicle__c.Model_SKU__c` | **Picklist — 12 SKUs** (from `svt_product_catalog.csv`) |
| Product catalog in Salesforce | **No** — stays Data Cloud / picklist values only |
| `vehicle_service_history.csv` (Data Cloud) | **Unchanged** — `preferred_dealer` remains text |
| Recommend Dealer / Create Task Flows | **Do not modify** |
| Lead agent / instructions | **Do not modify** |
| `Service_Visit__c` | **Defer** until Contact → Vehicle → Console works |

---

## Architecture (two paths)

```text
LEAD PATH (unchanged)
  Data Cloud → Recommend Dealer → dealerName (text) → Create Task → Agent

RIDER PATH (new)
  Contact → Vehicle__c → Preferred_Dealer__c → Account
                        → Model_SKU__c (12 SKUs)
                        → Advisor Console (LWC in 2D)
```

---

## Build sequence

### 2A — Dealer CRM foundation

1. On **Account**, create **`Dealer_ID__c`** (Text, External ID, Unique)
2. Import **`svt_dealer_accounts_import.csv`** (7 dealers)
3. Verify names match `dealer_directory.csv` `dealer_name` values

### 2B — Vehicle CRM foundation

Create **`Vehicle__c`** with fields:

| Field | API | Type |
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

**Model_SKU__c picklist values:** copy from `model_sku` column in `svt_product_catalog.csv`

3. Add **Vehicles** related list on Contact layout

### 2C — Vehicle data load

Source: **`vehicle_service_history.csv`** → import via **`svt_vehicles_crm_import.csv`**

| Import column | Resolves to |
|---|---|
| `Primary_Rider_Email` | Contact (must exist — from `riders.csv` / CRM) |
| `Preferred_Dealer_Dealer_ID__c` | Account via `Dealer_ID__c` |
| `Vehicle_Number__c` | Matches `vehicle_id` in Data Cloud |

**Import options:**

- Data Loader / Data Import Wizard with upsert on `Vehicle_Number__c`
- Or Flow/script: match Contact by email, Account by `Dealer_ID__c`

**Prerequisite:** 6 rider **Contacts** exist (Ananya, Vikram, Meera, Arjun, Nisha, Rahul)

### 2D — Dynamic LWC (after 2C verified)

Replace hardcoded vehicle fields on Advisor Console with:

- Query `Vehicle__c` where `Primary_Rider__c = contactId`
- Display Model SKU, VIN, Odometer, Preferred Dealer (Account name)

**Only after 2D works** → wire Agentforce / copilot to console context (if desired)

---

## Import files

| File | Purpose |
|---|---|
| `svt_dealer_accounts_import.csv` | Step 2A — 7 dealer Accounts |
| `svt_vehicles_crm_import.csv` | Step 2C — 6 vehicles |
| `svt_product_catalog.csv` | Picklist value source (no CRM import required) |
| `vehicle_service_history.csv` | Data Cloud only — **do not change** |

---

## Explicit do-not-touch list

- SVT Get Lead Context V2
- SVT Get Lead Intent v2
- SVT Recommend Dealer
- SVT Create Lead Test Ride Task
- Lead Engagement subagent instructions
- Data Cloud data streams (including dealer directory)
- Streaming Ingestion API
- Data Library / Path A PDFs

---

## Verification (2C complete)

| Contact | Vehicle Number | Model SKU | Dealer Account |
|---|---|---|---|
| ananya.rao@example.test | SVT-VEH-2001 | SVT Stride 200 Demo | SVT Bengaluru Central |
| vikram.mehta@example.test | SVT-VEH-2002 | SVT Stride 200 Pro | SVT Pune West |
| meera.iyer@example.test | SVT-VEH-2003 | SVT Urban 125 Demo | SVT Chennai North |
| arjun.kapoor@example.test | SVT-VEH-2004 | SVT Pulse 160 Standard | SVT Delhi South |
| nisha.patel@example.test | SVT-VEH-2005 | SVT Nova 110 Lite | SVT Ahmedabad One |
| rahul.nair@example.test | SVT-VEH-2006 | SVT Apex 300 Sport | SVT Kochi Central |

Open **Ananya Rao** → related Vehicles → one record with odometer **10400**.

---

*Synthetic SVT Motors demo*
