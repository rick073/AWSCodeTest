# AWSCodeTest
A Python script that parses Atlassian IP address ranges and updates an AWS security group. The script primarily uses the boto3 SDK and the JSON library, with support from the urllib and socket libraries.

The script is designed to run off of an AWS Lambda.

It first reads the list of IP ranges from the website using urllib, loading them into a dictionary allIpRanges. It then iterates through all of the dictionaries under the "items" key of allIpRanges, getting the CIDR IP.

It then checks to see if the IP address is IPv4 or IPv6 by attempting to convert the IP from IPv4 to binary form using the socket.inet_aton() method. If the method produces an error, then the IP is IPv6, and is added to the list of IPv6 ranges. If the method does not produce an error, then the IP is IPv4, and is added to the list of IPv4 ranges. This is neccesary because IPv4 and IPv6 are handled differently in the boto3's authorize_security_group_ingress() method, and must be separated.

The script then constructs the list of IP permissions to be added to the AWS security group rules. All of the IPs will be given ingress permissions using TCP protocol and port 80, which are hard coded into the code for the purpose of the exercise. Updating the AWS security group is carried out by boto3's authorize_security_group_ingress() method.

The AWS EC2 setup script is included in the script. The security group was created using all default settings using boto3's create_security_group() method.