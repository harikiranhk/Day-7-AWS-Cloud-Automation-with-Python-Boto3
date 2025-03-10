import boto3

region = "us-east-1"
ec2 = boto3.client("ec2", region_name=region)

# Get all instances
instances = ec2.describe_instances()
instance_ids = [i["InstanceId"] for r in instances["Reservations"] for i in r["Instances"]]

def control_instances(action):
    if action == "start":
        ec2.start_instances(InstanceIds=instance_ids)
        print("Starting instances...")
    elif action == "stop":
        ec2.stop_instances(InstanceIds=instance_ids)
        print("Stopping instances...")

# Call function
control_instances("stop")  # Change to "start" to start instances