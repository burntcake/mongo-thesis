import boto3
from botocore.exceptions import ClientError
from config import *

class MongoReplicaSet:
    def __init__(self, instance_type, region_name, instance_id_list):
        key, skey = self.get_credential()
        self.client = boto3.client(instance_type, region_name=region_name, aws_access_key_id=key, aws_secret_access_key=skey)
        self.instance_id_list = instance_id_list

    def get_credential(self):
        with open(AWS_CREDENTIAL) as f:
            content = f.readlines()
        lines = [x.strip() for x in content]
        key = lines[1].split("=")[1]
        skey = lines[2].split("=")[1]
        return key, skey

    def start_all(self):
        for instance_id in self.instance_id_list:
            try:
                self.client.start_instances(InstanceIds=[instance_id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

                # Dry run succeeded, run start_instances without dryrun
            try:
                response = self.client.start_instances(InstanceIds=[instance_id], DryRun=False)
                print(response)
            except ClientError as e:
                print(e)

    def stop_all(self):
        for instance_id in self.instance_id_list:
            try:
                self.client.stop_instances(InstanceIds=[instance_id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

                # Dry run succeeded, call stop_instances without dryrun
            try:
                response = self.client.stop_instances(InstanceIds=[instance_id], DryRun=False)
                print(response)
            except ClientError as e:
                print(e)


if __name__ == '__main__':
    mongo = MongoReplicaSet(AWS_RESOURCE_TYPE, AWS_REGION_NAME,
                            AWS_INSTANCE_ID_LIST)
    while 1:
        arg = input("Enter 0 to stop all instances\n" +
                    "Enter 1 to start all instances\n"+
                    "Enter e to exit\n\nCommand: ")

        if arg == "0":
            mongo.stop_all()
            break
        elif arg == "1":
            mongo.start_all()
            break
        elif arg == "e":
            break
        else:
            "Invalid input!\n"

