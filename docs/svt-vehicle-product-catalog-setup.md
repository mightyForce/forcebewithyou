# SVT product catalog — how to use `svt_product_catalog.csv`

**File:** [`svt-demo-data/svt_product_catalog.csv`](svt-demo-data/svt_product_catalog.csv)  
**Contents:** 6 base models × 2 variants = **12 SKUs** with specs

You **do not need a Data Cloud data stream** for this file if your goal is only **CRM Vehicle picklists**. The CSV is the master list of allowed model/variant values.

---

## Three ways to use the catalog

| Approach | Best for | Data Cloud stream? |
|---|---|---|
| **A. CRM picklists on `Vehicle__c`** | Dealer enters owned/interest vehicle on Lead/Contact | **No** |
| **B. CRM custom object `SVT Product__c`** | Lookup + specs on Vehicle; easy to add SKUs later | **No** |
| **C. Data Cloud DMO + Flow** | Agent **`SVT Get Model Specs`** returns battery/range by SKU | **Yes** (optional) |

Your screenshot shows streams for prospects, dealer directory, engagement, etc. — **`svt_product_catalog.csv` is not required there** unless you choose **C** for agent spec lookup.

---

## Option A — Vehicle custom object with picklists (recommended for your case)

### Object: `Vehicle__c`

| Field | Type | Purpose |
|---|---|---|
| `Name` | Auto or Text | e.g. `SVT-VEH-2001` |
| `Contact__c` | Lookup(Contact) | Rider ownership |
| `Lead__c` | Lookup(Lead) | Prospect interest (optional) |
| `Base_Model__c` | **Picklist** (6 values) | User picks base model first |
| `Variant__c` | **Dependent picklist** | Values depend on base model |
| `Model_SKU__c` | Formula (Text) or Picklist | Full SKU for Flows/agent |

### Picklist: `Base_Model__c` (6 values)

```text
Stride 200
Urban 125
Pulse 160
Nova 110
Apex 300
Glide 90
```

### Dependent picklist: `Variant__c`

| Base model | Allowed variants |
|---|---|
| Stride 200 | Demo, Pro |
| Urban 125 | Demo, Plus |
| Pulse 160 | Standard, Long Range |
| Nova 110 | Lite, Connect |
| Apex 300 | Sport, Tour |
| Glide 90 | Eco, Family |

Configure in **Setup → Object Manager → Vehicle → Fields → Variant → Field Dependencies**.

### Formula `Model_SKU__c` (optional)

Build the same string as `model_sku` in the CSV, e.g.:

```text
"SVT " & TEXT(Base_Model__c) & " " & TEXT(Variant__c)
```

**Note:** Variant labels must match formula logic (e.g. `Long Range` not `LongRange`). Use exact labels from the CSV `variant` column.

### Single picklist alternative (simpler)

One field **`Model_SKU__c`** picklist with all **12 values** (no dependency):

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

Copy directly from the `model_sku` column in the CSV.

---

## Option B — CRM `SVT Product__c` reference object

Create a custom object with **12 records** (one per SKU). Import using [`svt_product_catalog_crm.csv`](svt-demo-data/svt_product_catalog_crm.csv).

| CRM field | CSV column |
|---|---|
| `Name` | `model_sku` |
| `Base_Model__c` | `base_model` |
| `Variant__c` | `variant` |
| `Battery_kWh__c` | `battery_kwh` |
| `Motor_Peak_kW__c` | `motor_peak_kw` |
| `Range_km__c` | `range_km` |
| … | … |

On **`Vehicle__c`**: lookup **`Product__c`** → `SVT Product__c`. Picklists stay in sync because users pick a catalog record, not free text.

**Pros:** Specs live in CRM; no Data Cloud stream; one place to add SKUs.  
**Cons:** Extra object + page layout work.

---

## Option C — Data Cloud stream (only if agent needs specs)

Use when you build **`SVT Get Model Specs`** Flow for the copilot.

1. **Data Streams → New → File Upload** → `svt_product_catalog.csv`
2. Map to custom DMO **`SVT Product Catalog`**
3. Primary key: **`model_sku`**
4. Add `source_system` if your org requires it (value: `ProductCatalog`)

| CSV column | DMO field type |
|---|---|
| `model_sku` | Text (PK) |
| `base_model` | Text |
| `variant` | Text |
| `battery_kwh` | Number |
| `motor_peak_kw` | Number |
| `range_km` | Number |
| `charge_min_0_80` | Number |
| `warranty_battery_years` | Number |
| `warranty_vehicle_years` | Number |

Agent reads specs from Flow; **Vehicle picklists on CRM are still separate** (Option A or B).

---

## How this fits your current demo

```text
Today (built):
  prospects.csv preferred_model  → Individual (Data Cloud)
  dealer_directory.csv model       → Recommend Dealer Flow
  lead_intent_events model         → Get Lead Intent Flow

Optional Vehicle__c (CRM):
  Base_Model__c + Variant__c       → owned vehicle on Contact (Ananya, etc.)
  Model_SKU__c                     → aligns with preferred_model on Lead

Optional product catalog:
  CRM picklists only               → no new data stream
  OR Data Cloud DMO                → agent spec questions
```

**Individual `preferred_model`** in Data Cloud can stay as full SKU text (already in `prospects.csv`). Vehicle picklists on CRM give advisors a **structured UI** for the same 12 values.

---

## Quick start (picklists only — ~20 min)

1. Create **`Vehicle__c`** with `Contact__c`, `Base_Model__c`, `Variant__c` (dependent)
2. Enter the 6 + 12 picklist values from tables above
3. Add **`Vehicle__c`** related list on Contact (Ananya Rao)
4. Manually create one vehicle per rider using [`vehicle_service_history.csv`](svt-demo-data/vehicle_service_history.csv) `vehicle_model` column
5. **Skip** Data Cloud stream for product catalog

---

## Spec reference (all 12 SKUs)

| model_sku | battery_kWh | motor_kW | range_km |
|---|---|---|---|
| SVT Stride 200 Demo | 3.2 | 4.2 | 142 |
| SVT Stride 200 Pro | 4.0 | 5.0 | 165 |
| SVT Urban 125 Demo | 1.8 | 2.8 | 95 |
| SVT Urban 125 Plus | 2.2 | 3.2 | 110 |
| SVT Pulse 160 Standard | 2.5 | 3.5 | 115 |
| SVT Pulse 160 Long Range | 3.0 | 3.5 | 140 |
| SVT Nova 110 Lite | 1.4 | 2.2 | 80 |
| SVT Nova 110 Connect | 1.6 | 2.5 | 88 |
| SVT Apex 300 Sport | 4.5 | 6.2 | 130 |
| SVT Apex 300 Tour | 5.2 | 5.8 | 170 |
| SVT Glide 90 Eco | 1.2 | 1.8 | 70 |
| SVT Glide 90 Family | 1.5 | 2.0 | 78 |

Full file: [`svt_product_catalog.csv`](svt-demo-data/svt_product_catalog.csv)

---

*Synthetic SVT Motors demo — not production guidance*
