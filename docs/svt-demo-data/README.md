# SVT demo data — model catalog and prospect matrix

**Version:** 2026.2 — 6 base models, 12 variants (SKUs), 12 prospects

---

## Product catalog (`svt_product_catalog.csv`)

| Base model | Variant A | Variant B |
|---|---|---|
| Stride 200 | Demo | Pro |
| Urban 125 | Demo | Plus |
| Pulse 160 | Standard | Long Range |
| Nova 110 | Lite | Connect |
| Apex 300 | Sport | Tour |
| Glide 90 | Eco | Family |

**12 SKUs** — full specs in `svt_product_catalog.csv`

---

## Prospect matrix (`prospects.csv`)

| Prospect | prospect_id | Model SKU | Intent | City | Dealer | Consent | Task |
|---|---|---|---|---|---|---|---|
| Isha Sharma | LEAD-2001 | SVT Stride 200 Demo | HIGH | Bengaluru | SVT Bengaluru Central | true | Allowed |
| Karan Singh | LEAD-2002 | SVT Stride 200 Pro | MEDIUM | Pune | SVT Pune West | true | Allowed |
| Aditi Menon | LEAD-2003 | SVT Urban 125 Demo | MEDIUM | Chennai | SVT Chennai North | false | Blocked |
| Rohit Verma | LEAD-2004 | SVT Urban 125 Plus | LOW | Delhi | SVT Delhi South | true | Allowed |
| Naveen Kumar | LEAD-2005 | SVT Pulse 160 Standard | HIGH | Bengaluru | SVT Bengaluru Central | true | Allowed |
| Vikram Patel | LEAD-2006 | SVT Pulse 160 Long Range | MEDIUM | Pune | SVT Pune West | true | Allowed |
| Sneha Reddy | LEAD-2007 | SVT Nova 110 Lite | MEDIUM | Chennai | SVT Chennai North | false | Blocked |
| Arjun Mehta | LEAD-2008 | SVT Nova 110 Connect | LOW | Delhi | SVT Delhi South | true | Allowed |
| Lakshmi Iyer | LEAD-2009 | SVT Apex 300 Sport | MEDIUM | Bengaluru | SVT Bengaluru Central | true | Allowed |
| Ravi Krishnan | LEAD-2010 | SVT Apex 300 Tour | HIGH | Hyderabad | SVT Hyderabad Central | true | Allowed |
| Pooja Desai | LEAD-2011 | SVT Glide 90 Eco | MEDIUM | Ahmedabad | SVT Ahmedabad One | true | Allowed |
| Manish Joshi | LEAD-2012 | SVT Glide 90 Family | LOW | Kochi | SVT Kochi Central | true | Allowed |

**False lead test:** `priya.nair@example.test` — not in dataset

---

## Existing riders (`vehicle_service_history.csv`)

| Rider | customer_id | Owned model |
|---|---|---|
| Ananya Rao | SVT-1001 | SVT Stride 200 Demo |
| Vikram Mehta | SVT-1002 | SVT Stride 200 Pro |
| Meera Iyer | SVT-1003 | SVT Urban 125 Demo |
| Arjun Kapoor | SVT-1004 | SVT Pulse 160 Standard |
| Nisha Patel | SVT-1005 | SVT Nova 110 Lite |
| Rahul Nair | SVT-1006 | SVT Apex 300 Sport |

---

## Data files

| File | Rows | Purpose |
|---|---|---|
| `svt_product_catalog.csv` | 12 | Model + variant specs |
| `dealer_directory.csv` | 84 | 7 dealers × 12 SKUs |
| `prospects.csv` | 12 | Prospect profiles |
| `lead_intent_events.csv` | 24 | Website engagement / intent |
| `vehicle_service_history.csv` | 6 | Rider service context |
| `riders.csv` | 6 | CRM rider profiles |
| `digital_engagement.csv` | 8 | Rider marketing engagement |
| `crm_leads_import_new.csv` | 12 | CRM Lead import |

---

## Data Cloud ingest order

1. `svt_product_catalog.csv` → **SVT Product Catalog** DMO (new)
2. `dealer_directory.csv` → **SVT Dealer Directory**
3. `prospects.csv` → **Individual** (+ contact points)
4. `lead_intent_events.csv` → **Website Engagement**
5. Rider files unchanged mapping

Re-import or replace streams after updating org data.

---

## Demo script changes

- **Naveen** is now **Pulse 160 Standard** (not Stride 200) — still HIGH, Bengaluru
- **Rohit** is now **Urban 125 Plus** (not Stride 200) — still LOW, Delhi
- **New leads:** Ravi (Hyderabad), Pooja (Ahmedabad), Manish (Kochi)

Primary anchors unchanged: **Isha** (HIGH), **Karan** (MEDIUM), **Aditi** (consent block)
