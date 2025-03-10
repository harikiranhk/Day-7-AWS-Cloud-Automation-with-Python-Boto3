import boto3

s3 = boto3.client("s3")
bucket_name = "my-bucket"

# Define lifecycle rule
lifecycle_configuration = {
    "Rules": [
        {
            "ID": "MoveToGlacier",
            "Prefix": "",
            "Status": "Enabled",
            "Transitions": [
                {
                    "Days": 30,
                    "StorageClass": "GLACIER"
                }
            ]
        }
    ]
}

# Apply policy
s3.put_bucket_lifecycle_configuration(
    Bucket=bucket_name,
    LifecycleConfiguration=lifecycle_configuration
)
print("Lifecycle policy applied successfully.")