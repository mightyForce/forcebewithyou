# SVT demo — AWS S3 PDF ingest + Search Index Easy Setup

**Purpose:** Ingest Path B PDFs from Amazon S3 into Data Cloud, then create a Search Index via **Easy Setup**.

**Pilot reference:** [svt-rag-pilot-v1-reference.md](svt-rag-pilot-v1-reference.md)

**Start with one file:** `docs/svt-rag-data-cloud/SVT_Stride_200_Technical_Specification.pdf`

---

## Architecture

```text
AWS S3 bucket (PDFs)
  → Data Cloud S3 connection
  → UDLO (unstructured data lake object)
  → UDMO (unstructured data model object)
  → File notification pipeline (keeps in sync)
  → Search Index (Easy Setup)
  → Retriever → Agent (later)
```

---

## Part 1 — AWS setup (~15 min)

### 1.1 Create S3 bucket

1. Log in to **AWS Console → S3 → Create bucket**
2. **Bucket name:** e.g. `svt-demo-rag-unstructured` (globally unique)
3. **Region:** note it (e.g. `ap-south-1` Mumbai or `us-east-1`) — must match Data Cloud connection
4. **Block Public Access:** keep all blocked (private bucket)
5. Create bucket

### 1.2 Create folder and upload PDF

1. Open the bucket → **Create folder:** `svt-rag/`
2. Upload **`SVT_Stride_200_Technical_Specification.pdf`** into `svt-rag/`

Full S3 path example:

```text
s3://svt-demo-rag-unstructured/svt-rag/SVT_Stride_200_Technical_Specification.pdf
```

### 1.3 IAM user for Data Cloud (minimum demo)

1. **IAM → Users → Create user** (e.g. `salesforce-datacloud-s3`)
2. Attach policy with at least:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetObject"],
      "Resource": [
        "arn:aws:s3:::svt-demo-rag-unstructured",
        "arn:aws:s3:::svt-demo-rag-unstructured/*"
      ]
    }
  ]
}
```

3. Create **Access Key** → save **Access Key ID** and **Secret Access Key**

> File notifications (Part 4) need extra IAM/Lambda permissions. Part 1–3 can work for initial POC; add notifications for refresh when PDFs change.

---

## Part 2 — Salesforce: Amazon S3 connection

1. **Setup → Data Cloud Setup** (or **Data Cloud → Setup**)
2. Search **Amazon S3** or open **Connections**
3. **New Connection → Amazon S3**
4. Enter:

| Field | Value |
|---|---|
| Connection name | `SVT S3 Unstructured` |
| Access Key ID | From IAM user |
| Secret Access Key | From IAM user |
| Bucket name | `svt-demo-rag-unstructured` |
| Region | Your bucket region |

5. **Test connection → Save**

If **Test** fails: check bucket name, region, IAM policy, and that keys are active.

---

## Part 3 — Create UDLO + UDMO (ingest PDF)

1. **App Launcher → Data Cloud**
2. **Data Lake Objects → New**
3. Select **From External Files → Next**
4. Choose **Amazon S3 → Next**
5. **Select Connection:** `SVT S3 Unstructured`
6. **Directory:** `svt-rag/`  
   (must match the folder where you uploaded the PDF; include trailing slash if the UI expects it)
7. **Next**
8. **UDLO name:** `SVT Reference Documents`
9. **Data Space:** `default`
10. **UDMO mapping:** click **New**
    - **UDMO name:** `SVT Reference Documents`
11. **Search index checkbox:**
    - **Uncheck** if you want to run **Search Index → Easy Setup** manually (recommended for learning the wizard)
    - **Leave checked** if you want Salesforce to auto-create index with system defaults (skips Easy Setup)
12. **Save / Deploy**

Wait for deploy **Success**.

---

## Part 4 — File notification pipeline (required for sync)

Salesforce expects a **file notification pipeline** so Data Cloud knows when files are added or updated in S3.

**Official guide:** [Set Up Unstructured Data from Amazon S3](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awss3-udlo.html) — section *Send File Notifications from Amazon S3 to Data 360*

Summary:

| Step | Action |
|---|---|
| 1 | Create RSA key pair + certificate (`openssl`) |
| 2 | Create **Connected App** with digital signature + scopes: `api`, `refresh_token`, `cdp_ingest_api` |
| 3 | Download Salesforce **S3 file notification installer script** |
| 4 | Configure `input_parameters_s3.conf` (bucket, region, org URL, consumer key) |
| 5 | Run `./setup_s3_file_notification.sh` |
| 6 | Upload PDF to S3 **after** pipeline exists (or re-upload to trigger notification) |

**POC shortcut:** If chunks do not appear after Part 3, complete Part 4 or re-upload the PDF to S3 after the pipeline is live.

---

## Part 5 — Search Index Easy Setup

**Prerequisite:** UDMO `SVT Reference Documents` exists and contains the PDF (check Data Explorer).

1. **Data Cloud → Search Indexes → New**
2. **Easy Setup → Next**
3. **Data Space:** `default`
4. **Select UDMO:** `SVT Reference Documents`
5. **Configuration Name:** `SVT Reference Library Index`
6. **API Name:** `SVT_Reference_Library_Index`
7. **Next → Review defaults:**
   - Chunking: Passage extraction
   - Embedding: E5-Large V2
   - Search type: Hybrid
8. **Save**

Wait until **Refresh Status = Ready / Success** (5–20 min for one PDF).

---

## Part 6 — Validate

### Data Explorer

1. **Data Explorer → Data Lake Object**
2. Find **chunk** object related to your index (name often includes `chunk` or index name)
3. Confirm text snippets mention **3.2 kWh**, **142 km**, **Stride 200**

### Test query (Prompt Builder)

1. **Setup → Prompt Builder → New**
2. Add **Retriever:** `SVT Reference Library Index`
3. Prompt:

   > What is the battery capacity of the SVT Stride 200 Demo?

4. **Expected:** **3.2 kWh** with citation from the PDF

---

## Part 7 — Add remaining PDFs (after POC)

1. Upload B2–B5 to `s3://.../svt-rag/` (same folder)
2. File notification triggers refresh (or manual refresh on UDLO)
3. Search index refresh runs automatically or via **Refresh** on index record

| File |
|---|
| `SVT_Urban_125_Technical_Specification.pdf` |
| `SVT_Warranty_and_Service_Policy_2026.pdf` |
| `SVT_Service_Bulletin_SB-2026-04.pdf` |
| `SVT_Dealer_Directory_Operations_Guide.pdf` |

All PDFs in repo: `docs/svt-rag-data-cloud/`

---

## Troubleshooting

| Issue | Fix |
|---|---|
| UDLO empty | Directory path mismatch — verify `svt-rag/` vs actual S3 prefix |
| PDF not picked up | File must be `.pdf`; check UDLO file type filter |
| No chunks | Complete file notification pipeline; re-upload PDF |
| UDMO not in Easy Setup | UDLO deploy must succeed first |
| Index Failed | Try one small PDF; check Data Cloud limits |
| 403 on S3 connection | IAM policy or wrong region |

---

## Naming reference (SVT demo)

| Artifact | Name |
|---|---|
| S3 bucket | `svt-demo-rag-unstructured` |
| S3 folder | `svt-rag/` |
| S3 connection | `SVT S3 Unstructured` |
| UDLO / UDMO | `SVT Reference Documents` |
| Search index | `SVT Reference Library Index` |

---

## Org URL (your demo)

`https://org-nm-8f0c2c7b75-dev-ed.develop.my.salesforce.com`

---

*Pilot guide — synthetic SVT Motors demo only*
