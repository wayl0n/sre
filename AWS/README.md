# ec2_audit_script.py

This script will securely scan (using an assumed EC2 IAM instance profile that has Read Only access and is explicitly trusted by the remote environment) multiple AWS environments for all running EC2 instances, gather their Name, Instance ID, Instance Size and AMI (Amazon Machine Image) and post its findings to Confluence in an easily navigable page.

Benefits include cost savings and improving our security posture by knowing what exactly is running in each of our environments and if the Operating System is in need of upgrading

Environments are stored in a config.json file that contain the environment name, the ARN for the assumed role and the AWS Region