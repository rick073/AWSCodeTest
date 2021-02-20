import json
import boto3


def main():
    with open('ip-ranges.atlassian.json') as file:
        ipRanges = json.load(file)

    for ip in ipRanges["items"]:
        cidr = ip["cidr"]
        print(cidr)


if __name__ == '__main__':
    main()
