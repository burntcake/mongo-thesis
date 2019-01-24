import boto3
import sys
client = boto3.client('ssm')
instance_id = [sys.argv[1]]
print(instance_id)
commands = ['poweroff -f']
response = client.send_command(
    DocumentName="AWS-RunShellScript",
    Parameters={'commands': commands},
    InstanceIds=instance_id,
)
