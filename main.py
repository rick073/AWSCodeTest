import json
import boto3
from botocore.exceptions import ClientError


def main():
    # CREATE LAMBDA CLIENT
    client = boto3.client('lambda')

    try:
        # CREATE SECURITY GROUP
        response = client.create_security_group(GroupName="SampleGroup")
        securityGroupId = response["GroupId"]
        print("Security group created. Name = " + securityGroupId)

        # PARSE ATLASSIAN IP RANGES
        with open('ip-ranges.atlassian.json') as file:
            allIpRanges = json.load(file)

        ipRanges = []
        ipv6Ranges = []
        for ip in allIpRanges["items"]:
            cidr = ip["cidr"]

            # SEPARATE IPV4 FROM IPV6
            if ip["mask_len"] == 56:
                # CONSTRUCT IPV4 AND IPV6 RANGES
                ipv6Ranges += {'CidrIpv6': cidr}
            else:
                # CONSTRUCT IPV4 RANGES
                ipRanges += {'CidrIp': cidr}

        # CONSTRUCT IP_PERMISSIONS
        IPPermissions = {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': ipRanges, 'Ipv6Ranges': ipv6Ranges}

        # AUTHORIZE SECURITY GROUP INGRESS
        data = client.authorize_security_group_ingress(GroupId=securityGroupId, IpPermissions=IPPermissions)
        print("Ingress rules successfully set:\n" + data)

    except ClientError as e:
        print(e)


if __name__ == '__main__':
    main()
