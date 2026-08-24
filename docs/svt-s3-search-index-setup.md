# DEPRECATED — S3 + Search Index setup (Path B dropped)

> **Status:** Out of scope for the SVT demo as of v1.1 (24 Aug 2026).  
> **Use instead:** [SVT Document Grounding Reference — Path A only](svt-rag-pilot-v1-reference.md) (Agentforce Data Library).

Path B (Data Cloud unstructured ingest from Amazon S3, UDLO, file notification pipeline, Search Index, Retriever) has been **removed from the demo plan**. This file is kept for historical reference only.

---

## Why it was dropped

- Unstructured DLO + S3 file notifications added significant AWS/Lambda complexity
- Developer Edition demos run faster with **Agentforce Data Library** (~1 hour)
- Structured data (Flows + DMOs + Ingestion API) covers intent, dealer, and tasks
- Advisor one-pagers in Path A include summary specs and objection handling

---

## Active demo paths

| Need | Use |
|---|---|
| Intent, dealer, tasks, email | Structured Flows + Data Cloud DMOs |
| Live engagement events | Streaming Ingestion API data stream |
| Specs, playbook, objections | **Agentforce Data Library** — see [pilot reference](svt-rag-pilot-v1-reference.md) |

---

*Original Path B content archived in git history.*
