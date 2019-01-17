# code from https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-managing-instances.html
import sys
import boto3
from botocore.exceptions import ClientError

instance_id = sys.argv[1]

ec2 = boto3.client('ec2')

# Do a dryrun first to verify permissions
try:
    ec2.terminate_instances(InstanceIds=[instance_id], DryRun=True)
except ClientError as e:
    if 'DryRunOperation' not in str(e):
        raise

# Dry run succeeded, run start_instances without dryrun
try:
    response = ec2.terminate_instances(InstanceIds=[instance_id], DryRun=False)
    print(response)
except ClientError as e:
    print(e)

