import boto3
import os
import smtplib
from slack_sdk import WebClient

# AWS and Slack configuration
region = "us-east-1"
ec2 = boto3.client("ec2", region_name=region)

# Define email and Slack details
slack_token = "xoxb-your-slack-token"
slack_channel = "#alerts"
ses_email = "alert@example.com"
smtp_server = "smtp.example.com"

# Function to scan logs and send alerts
def scan_logs():
    for file in os.listdir("/var/log"):
        if file.endswith(".log"):
            with open(f"/var/log/{file}") as log_file:
                for line in log_file:
                    if "ERROR" in line:
                        send_alert(line)

# Send alerts via Slack and SES
def send_alert(message):
    client = WebClient(token=slack_token)
    client.chat_postMessage(channel=slack_channel, text=message)
    
    with smtplib.SMTP(smtp_server) as server:
        server.sendmail(ses_email, ses_email, message)

scan_logs()