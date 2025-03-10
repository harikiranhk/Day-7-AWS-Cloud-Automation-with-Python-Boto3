import boto3

domain = "example.com"
hosted_zone_id = "ZXXXXXXXXXXXX"
ip_address = "192.168.1.1"

route53 = boto3.client("route53")

# Update DNS record
response = route53.change_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    ChangeBatch={
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": f"subdomain.{domain}",
                    "Type": "A",
                    "TTL": 300,
                    "ResourceRecords": [{"Value": ip_address}]
                }
            }
        ]
    }
)

print("DNS record updated successfully.")