import boto3
from reportlab.pdfgen import canvas

cost_client = boto3.client("ce")
response = cost_client.get_cost_and_usage(
    TimePeriod={"Start": "2024-03-01", "End": "2024-03-31"},
    Granularity="MONTHLY",
    Metrics=["BlendedCost"]
)

total_cost = response["ResultsByTime"][0]["Total"]["BlendedCost"]["Amount"]

def generate_pdf(cost):
    pdf = canvas.Canvas("billing_report.pdf")
    pdf.drawString(100, 750, f"AWS Billing Report: ${cost}")
    pdf.save()

generate_pdf(total_cost)
print("Billing report generated successfully.")