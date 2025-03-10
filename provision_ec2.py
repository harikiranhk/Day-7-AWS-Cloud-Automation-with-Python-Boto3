import boto3
import paramiko
import time
import os

# Initialize Boto3 client
ec2 = boto3.client("ec2")

# Create key pair
key_name = "ec2-key-pair"
key_pair = ec2.create_key_pair(KeyName=key_name)
private_key = key_pair['KeyMaterial']

# Save the key pair
with open(f"{key_name}.pem", "w") as key_file:
    key_file.write(private_key)
os.chmod(f"{key_name}.pem", 0o400)

# Create security group
security_group = ec2.create_security_group(
    GroupName="ec2-security-group", Description="Allow SSH access"
)
security_group_id = security_group['GroupId']

ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

# Launch EC2 instance
instance = ec2.run_instances(
    ImageId="ami-0c55b159cbfafe1f0",  # Update with a valid AMI
    InstanceType="t2.micro",
    KeyName=key_name,
    SecurityGroupIds=[security_group_id],
    MinCount=1,
    MaxCount=1
)
instance_id = instance["Instances"][0]["InstanceId"]

# Wait for instance to be running
print("Waiting for instance to launch...")
boto3.resource("ec2").Instance(instance_id).wait_until_running()
instance_info = ec2.describe_instances(InstanceIds=[instance_id])
public_ip = instance_info["Reservations"][0]["Instances"][0]["PublicIpAddress"]

print(f"EC2 Instance launched successfully with Public IP: {public_ip}")

# Connect via SSH using Paramiko
time.sleep(60)  # Wait for SSH service to be available
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(public_ip, username="ec2-user", key_filename=f"{key_name}.pem")

stdin, stdout, stderr = ssh.exec_command("echo Connection Successful")
print(stdout.read().decode())

ssh.close()