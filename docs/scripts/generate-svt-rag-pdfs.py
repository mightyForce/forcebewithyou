#!/usr/bin/env python3
"""Generate SVT advisor PDFs for Agentforce Data Library (Path A only)."""
from pathlib import Path
from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = ROOT / "svt-rag-data-library"
FOOTER = "SVT Motors Demo - Synthetic Data Only - Not for Production Use"


class SVTPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, FOOTER, align="C")


def write_pdf(path: Path, title: str, sections: list[tuple[str, str]]):
    pdf = SVTPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, "Document ID: SVT-DEMO-RAG | Classification: Internal Advisor Use")
    pdf.ln(6)
    for heading, body in sections:
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 8, heading)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, body)
        pdf.ln(4)
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(path))
    print(f"Created {path}")


DOCS = {
    LIB_DIR / "SVT_Advisor_Test_Ride_Playbook.pdf": (
        "SVT Advisor Test Ride Playbook",
        [
            ("Purpose", "Guide dealer advisors through scheduling and conducting SVT test rides. Use with SVT Advisor Copilot after intent qualification."),
            ("Before the Ride", "Confirm valid driving license. Confirm helmet availability. Confirm appointment date/time with prospect. Verify contact consent is true in Data Cloud before sending customer email."),
            ("During the Ride (15 minutes)", "Recommended route: mixed city and quiet road. Highlight regen braking, display cluster, and storage. Do not promise discounts or financing terms."),
            ("After the Ride", "Create CRM Task within 24 hours (subject prefix: Test Ride). Send confirmation email if consent allows. Schedule follow-up call within 48 hours."),
            ("Do Not", "Do not approve pricing. Do not guarantee delivery dates. Do not bypass consent guardrails."),
        ],
    ),
    LIB_DIR / "SVT_Stride_200_Advisor_OnePager.pdf": (
        "SVT Stride 200 Demo - Advisor One-Pager",
        [
            ("Positioning", "Premium urban electric scooter for professionals who want range confidence and smart connectivity."),
            ("Top Features", "- 3.2 kWh battery\n- Smart TFT display\n- Regenerative braking\n- App-based diagnostics\n- Fast charge: 0-80% in 45 min (demo conditions)"),
            ("Ideal Buyer", "Daily commuters in Bengaluru, Pune, Delhi metro areas. First-time EV upgraders."),
            ("Good For Demo Leads", "Isha Sharma, Naveen Kumar, Karan Singh, Lakshmi Iyer, Rohit Verma (LOW intent still eligible for nurture)."),
            ("Do Not Claim", "Do not quote exact on-road price. Use only the specs listed in this one-pager; if not listed, say it is not in the approved SVT documents."),
        ],
    ),
    LIB_DIR / "SVT_Urban_125_Advisor_OnePager.pdf": (
        "SVT Urban 125 Demo - Advisor One-Pager",
        [
            ("Positioning", "Lightweight city scooter for short urban trips and easy parking."),
            ("Top Features", "- 1.8 kWh battery\n- Lightweight frame\n- City ride modes\n- USB charging port\n- Swappable battery option (select markets)"),
            ("Ideal Buyer", "City dwellers, students, short-distance commuters in Chennai and dense urban PINs."),
            ("Good For Demo Leads", "Aditi Menon, Sneha Reddy (check contact consent before task or email)."),
            ("Do Not Claim", "Do not compare unfavourably to competitors by name. Refer to objection handling guide for price conversations."),
        ],
    ),
    LIB_DIR / "SVT_Objection_Handling_Guide.pdf": (
        "SVT Objection Handling Guide",
        [
            ("Too Expensive", "Acknowledge budget concern. Reframe total cost of ownership: lower running cost vs petrol. Offer test ride before price discussion. Do NOT approve discounts - escalate to sales manager."),
            ("Range Anxiety", "Explain demo range figures are under ideal conditions. Point to technical specification for battery kWh and certified range. Suggest test ride to experience regen braking."),
            ("I Will Think About It", "Ask what information would help decide. Offer dealer follow-up within 48 hours. Create CRM task only with consent."),
            ("Competitor Mention", "Focus on SVT test ride experience and service network. Do not disparage competitors."),
            ("Authority Reminder", "Advisors may explain value. Only authorized finance team may approve financing or discounts."),
        ],
    ),
}


def main():
    for path, (title, sections) in DOCS.items():
        write_pdf(path, title, sections)


if __name__ == "__main__":
    main()
