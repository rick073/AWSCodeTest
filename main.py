import json
import urllib.request
import boto3
import socket
from botocore.exceptions import ClientError


JSON_URL = "https://ip-ranges.atlassian.com/"
SEC_GROUP_ID = "sg-04066ff7ffcbb1a3b"


def lambda_handler(event, context):
	# CREATE LAMBDA CLIENT
	client = boto3.client('ec2')

	try:
		# CREATE SECURITY GROUP
		# response = client.create_security_group(GroupName="SampleGroup", Description="SampleGroupDescription")
		# SEC_GROUP_ID = response["GroupId"]
		# print("Security group created. Name = " + SEC_GROUP_ID)

		# PARSE ATLASSIAN IP RANGES
		jsonurl = urllib.request.urlopen(JSON_URL)
		allIpRanges = json.loads(jsonurl.read().decode())

		ipRanges = []
		ipv6Ranges = []
		for ip in allIpRanges["items"]:
			cidr = ip["cidr"]

			try:
				# SEPARATE IPV4 FROM IPV6
				socket.inet_aton(ip["network"])
				# CONSTRUCT IPV4 RANGES
				ipRanges.append({'CidrIp': cidr})
			except socket.error:
				# CONSTRUCT IPV6 RANGES
				ipv6Ranges.append({'CidrIpv6': cidr})

		# CONSTRUCT IP_PERMISSIONS
		IPPermissions = [{'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': ipRanges, 'Ipv6Ranges': ipv6Ranges}]

		# AUTHORIZE SECURITY GROUP INGRESS
		data = client.authorize_security_group_ingress(GroupId=SEC_GROUP_ID, IpPermissions=IPPermissions)
		print("Ingress rules successfully set:\n %s" % data)

	except ClientError as e:
		print(e)

	return 0
