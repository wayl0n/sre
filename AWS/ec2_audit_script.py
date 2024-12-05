#!/usr/bin/env python3

from atlassian import Confluence
import boto3
from bs4 import BeautifulSoup, Tag
import json
import os
import re
import requests

os.system ("clear")

# Global vars
conUser = "your confluence API unprivileged username"
conPass = "your confluence API unprivileged pass"
pageid  = 'your page ID in Confluence'
conf_url = 'https://your_confluence_url'

envs_aws_detailed_dict = {}

def connect_to_envs():

  with open('config.json') as data_file:

    data = json.load(data_file)

    for key, value in sorted(data.items()):

      print (key)
      role_arn = data[key]['ARN']
      print (role_arn)
      region = data[key]['Region']
      print (region)

      session = boto3.Session()
      sts = session.client("sts")
      response = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="sre-audit-robot"
      )
      # print(response)

      new_session = boto3.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                      aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                      aws_session_token=response['Credentials']['SessionToken'])

      # create filter to only get running EC2 instances
      filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
      ]

      ec2 = new_session.resource('ec2', region)
      instances = ec2.instances.filter(Filters=filters)
      # print(instances)
      # print (type(instances))

      envs_aws_detailed_dict[key] = {}

      for instance in instances:

        print (instance)
        print (instance.id)

        envs_aws_detailed_dict[key][instance.id] = []

        print (instance.instance_type)

        try:

          for tags in instance.tags:

            if tags["Key"] == 'Name':

                # print ("We found an EC2 Instance that has a tag called Name:")
                vm_name = tags['Value']
                # print (vm_name + '\n')
                # print ("-------\n")
                envs_aws_detailed_dict[key][instance.id].append(vm_name)

        except Exception:

          pass

        envs_aws_detailed_dict[key][instance.id].append(instance.instance_type)

        try:

          print (instance.image.name)
          envs_aws_detailed_dict[key][instance.id].append(instance.image.name)

        except Exception:

          envs_aws_detailed_dict[key][instance.id].append("AMI Name Not Found")

  return envs_aws_detailed_dict

def publish_to_confluence_all_instances(envs_aws_detailed_dict):

  body = '<p><ac:structured-macro ac:name="toc"/></p>'

  for key in envs_aws_detailed_dict.keys():

    print (key)

    body = body + "<H2>" + key + "</H2>"

    body = body + '<ac:structured-macro ac:name="expand">'

    body = body + '<ac:parameter ac:name="title">Click to expand</ac:parameter>'

    body = body + "<ac:rich-text-body>"

    body = body + "<table><tbody><tr><th>EC2 Instance Name</th><th>EC2 Instance ID</th><th>EC2 Instance Size</th><th>EC2 AMI Name</th></tr>"

    for k, v in sorted(envs_aws_detailed_dict[key].items(), key=lambda e: e[1]):

      print ( k,v )

      body = body +  "<tr><td>" + v[0] + "</td>"

      body = body +  "<td>" + k.upper() + "</td>"

      body = body +  "<td>" + v[1] + "</td>"

      body = body +  "<td>" + v[2] + "</td></tr>"

    body = body + "</tbody>"

    body = body + "</table>"

    body = body + "</ac:rich-text-body>"

    body = body + "</ac:structured-macro>"

  # Connect to Confluence to publish info
  confluence = Confluence(url=conf_url,
  username=conUser,
  password=conPass)

  title = "Currently Running Cloud EC2 Instances per Environment"

  confluence.update_page(pageid, title, body, parent_id=None, type='page', representation='storage', minor_edit=False, full_width=False)

# Gather EC2 Instances in AWS per Env
connect_to_envs()

# Publish All Running EC2 Instances in AWS to Confluence
publish_to_confluence_all_instances(envs_aws_detailed_dict)
