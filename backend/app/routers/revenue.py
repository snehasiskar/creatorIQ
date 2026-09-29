from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from io import BytesIO
import csv
from datetime import date, timedelta

from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


router = APIRouter(
    prefix="/revenue",
    tags=["Revenue Analytics"]
)


# ---------------------------------------------------------
# Sample revenue data
# ---------------------------------------------------------

revenue_data = [
    {
        "source": "Sponsorship",
        "amount": 2500,
        "month": "January"
    },
    {
        "source": "Ad Revenue",
        "amount": 1800,
        "month": "January"
    },
    {
        "source": "Affiliate Marketing",
        "amount": 950,
        "month": "January"
    },
    {
        "source": "Subscription",
        "amount": 700,
        "month": "January"
    },
    {
        "source": "Sponsorship",
        "amount": 3200,
        "month": "February"
    },
    {
        "source": "Ad Revenue",
        "amount": 2100,
        "month": "February"
    },
    {
        "source": "Affiliate Marketing",
        "amount": 1100,
        "month": "February"
    },
    {
        "source": "Subscription",
        "amount": 850,
        "month": "February"
    },
    {
        "source": "Sponsorship",
        "amount": 4100,
        "month": "March"
    },
    {
        "source": "Ad Revenue",
        "amount": 2500,
        "month": "March"
    },
    {
        "source": "Affiliate Marketing",
        "amount": 1350,
        "month": "March"
    },
    {
        "source": "Subscription",
        "amount": 1000,
        "month": "March"
    }
]


# ---------------------------------------------------------
# Sponsorship data
# ---------------------------------------------------------

sponsorships = [
    {
        "id": 1,
        "brand": "TechBrand",
        "campaign": "Creator Laptop Campaign",
        "amount": 2500,
        "status": "Paid",
        "due_date": "2026-01-15"
    },
    {
        "id": 2,
        "brand": "FashionHub",
        "campaign": "Summer Fashion Campaign",
        "amount": 3200,
        "status": "Pending",
        "due_date": "2026-10-05"
    },
    {
        "id": 3,
        "brand": "FitLife",
        "campaign": "Fitness Product Promotion",
        "amount": 4100,
        "status": "Pending",
        "due_date": "2026-10-12"
    }
]


class Sponsorship(BaseModel):
    brand: str
    campaign: str
    amount: float
    status: str = "Pending"
    due_date: str


# ---------------------------------------------------------
# Revenue summary
# ---------------------------------------------------------

@router.get("/summary")
def revenue_summary():

    total_revenue = sum(item["amount"] for item in revenue_data)

    sponsorship = sum(
        item["amount"]
        for item in revenue_data
        if item["source"] == "Sponsorship"
    )

    ads = sum(
        item["amount"]
        for item in revenue_data
        if item["source"] == "Ad Revenue"
    )

    affiliate = sum(
        item["amount"]
        for item in revenue_data
        if item["source"] == "Affiliate Marketing"
    )

    subscription = sum(
        item["amount"]
        for item in revenue_data
        if item["source"] == "Subscription"
    )

    return {
        "total_revenue": total_revenue,
        "sponsorship_revenue": sponsorship,
        "ad_revenue": ads,
        "affiliate_revenue": affiliate,
        "subscription_revenue": subscription,
        "currency": "USD"
    }


# ---------------------------------------------------------
# Revenue trends
# ---------------------------------------------------------

@router.get("/trends")
def revenue_trends():

    months = {}

    for item in revenue_data:
        month = item["month"]

        if month not in months:
            months[month] = 0

        months[month] += item["amount"]

    return {
        "labels": list(months.keys()),
        "values": list(months.values())
    }


# ---------------------------------------------------------
# Sponsorship tracking
# ---------------------------------------------------------

@router.get("/sponsorships")
def get_sponsorships():

    return {
        "count": len(sponsorships),
        "sponsorships": sponsorships
    }


@router.post("/sponsorships")
def add_sponsorship(sponsorship: Sponsorship):

    new_id = len(sponsorships) + 1

    new_sponsorship = {
        "id": new_id,
        **sponsorship.model_dump()
    }

    sponsorships.append(new_sponsorship)

    return {
        "message": "Sponsorship added successfully",
        "sponsorship": new_sponsorship
    }


# ---------------------------------------------------------
# Monetization report
# ---------------------------------------------------------

@router.get("/report")
def monetization_report():

    summary = revenue_summary()
    trends = revenue_trends()

    pending = [
        sponsorship
        for sponsorship in sponsorships
        if sponsorship["status"].lower() == "pending"
    ]

    return {
        "report": "CreatorIQ Monetization Report",
        "summary": summary,
        "revenue_trends": trends,
        "pending_sponsorships": pending,
        "total_sponsorship_contracts": len(sponsorships)
    }


# ---------------------------------------------------------
# Notifications / alerts
# ---------------------------------------------------------

@router.get("/notifications")
def revenue_notifications(
    target: float = Query(10000),
):

    summary = revenue_summary()

    notifications = []

    if summary["total_revenue"] >= target:
        notifications.append({
            "type": "success",
            "message": "Revenue target has been reached."
        })
    else:
        remaining = target - summary["total_revenue"]

        notifications.append({
            "type": "warning",
            "message": f"${remaining:.2f} remaining to reach revenue target."
        })

    for sponsorship in sponsorships:

        if sponsorship["status"].lower() == "pending":

            notifications.append({
                "type": "revenue",
                "message": (
                    f"Payment pending from {sponsorship['brand']} "
                    f"for ${sponsorship['amount']:.2f}."
                )
            })

    return {
        "notifications": notifications
    }


# ---------------------------------------------------------
# CSV export
# ---------------------------------------------------------

@router.get("/export/csv")
def export_csv():

    output = BytesIO()

    text_output = []

    header = ["Source", "Month", "Amount"]

    text_output.append(",".join(header))

    for item in revenue_data:

        text_output.append(
            f"{item['source']},{item['month']},{item['amount']}"
        )

    csv_data = "\n".join(text_output).encode("utf-8")

    output.write(csv_data)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=creatoriq_revenue_report.csv"
        }
    )


# ---------------------------------------------------------
# Excel export
# ---------------------------------------------------------

@router.get("/export/excel")
def export_excel():

    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = "Revenue Report"

    worksheet.append([
        "Source",
        "Month",
        "Amount"
    ])

    for item in revenue_data:

        worksheet.append([
            item["source"],
            item["month"],
            item["amount"]
        ])

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition":
            "attachment; filename=creatoriq_revenue_report.xlsx"
        }
    )


# ---------------------------------------------------------
# PDF export
# ---------------------------------------------------------

@router.get("/export/pdf")
def export_pdf():

    output = BytesIO()

    pdf = canvas.Canvas(
        output,
        pagesize=letter
    )

    pdf.setTitle(
        "CreatorIQ Revenue Report"
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        50,
        750,
        "CreatorIQ Revenue Report"
    )

    summary = revenue_summary()

    y = 710

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        50,
        y,
        f"Total Revenue: ${summary['total_revenue']:.2f}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Sponsorship Revenue: ${summary['sponsorship_revenue']:.2f}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Ad Revenue: ${summary['ad_revenue']:.2f}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Affiliate Revenue: ${summary['affiliate_revenue']:.2f}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Subscription Revenue: ${summary['subscription_revenue']:.2f}"
    )

    y -= 45

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        50,
        y,
        "Sponsorships"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    for sponsorship in sponsorships:

        line = (
            f"{sponsorship['brand']} - "
            f"{sponsorship['campaign']} - "
            f"${sponsorship['amount']:.2f} - "
            f"{sponsorship['status']}"
        )

        pdf.drawString(
            50,
            y,
            line
        )

        y -= 20

        if y < 50:

            pdf.showPage()
            y = 750

    pdf.save()

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=creatoriq_revenue_report.pdf"
        }
    )
