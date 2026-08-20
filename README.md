# forcebewithyou — Health Cloud Demo

A Salesforce Health Cloud demo environment using standard objects to simulate patient care management workflows.

## Quick Start

1. Open your Salesforce org (DotSolved Systems / Agentforce sandbox).
2. Search for **Summit Valley Medical Center** in Accounts.
3. Open any patient contact (`maria.lopez.demo@summitvalley.health`, etc.).
4. Review linked Cases (care plans) and Tasks (care activities).

## Demo Scenario

**Summit Valley Medical Center** coordinates care for three patients across chronic disease, post-surgical recovery, and senior wellness programs. Each patient has an active care plan (Case) with assigned tasks representing interventions.

| Patient | Care Plan | Priority |
|---------|-----------|----------|
| Maria Lopez | Diabetes Management | High |
| James Chen | Cardiac Recovery | High |
| Eleanor Whitmore | Senior Wellness | Medium |
| Robert Kim | COPD Management | High |
| Sarah Patel | Prenatal Care | High |
| David Morrison | Mental Health Support | Medium |
| Linda Foster | Oncology Survivorship | Medium |
| Carlos Rivera | Asthma Management | High |

## Repository Structure

```
demo/
  queries.soql       # SOQL queries for demo walkthrough
  seed-data.json        # Record IDs and demo data reference
  prospects-template.csv # CSV template for bulk import
  prospects-batch.json   # JSON batch template for ingestion
docs/
  HEALTH_CLOUD_DEMO.md  # Full demo script and Health Cloud mapping
  INGEST_PROSPECTS.md   # How to add more patients/prospects
```

## Health Cloud vs. This Demo

This org does not have Health Cloud licensed. The demo maps standard Salesforce objects to Health Cloud concepts:

| Health Cloud Object | Demo Mapping |
|---------------------|--------------|
| Person Account (Patient) | Contact |
| Care Plan | Case |
| Care Plan Goal | Task |
| Healthcare Provider | Account (Type: Healthcare Provider) |
| Payer | Account (Type: Payer) |

See [docs/HEALTH_CLOUD_DEMO.md](docs/HEALTH_CLOUD_DEMO.md) for the full walkthrough and upgrade path to native Health Cloud.

## Demo Queries

Run queries from `demo/queries.soql` in Developer Console or VS Code with Salesforce CLI.
