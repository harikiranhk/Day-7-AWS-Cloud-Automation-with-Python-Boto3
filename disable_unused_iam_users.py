import boto3
from datetime import datetime, timedelta

# Initialize IAM client
iam = boto3.client("iam")

# Define inactivity period (e.g., 90 days)
inactive_days = 90
time_threshold = datetime.utcnow() - timedelta(days=inactive_days)

# Get all IAM users
users = iam.list_users()["Users"]

for user in users:
    username = user["UserName"]
    last_used = iam.get_login_profile(UserName=username)
    
    if "CreateDate" in last_used:
        last_activity = last_used["CreateDate"]
        if last_activity < time_threshold:
            print(f"Disabling user: {username}")
            iam.delete_login_profile(UserName=username)
            iam.update_user(UserName=username, NewPath="/disabled/")