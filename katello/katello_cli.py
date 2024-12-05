#!/usr/bin/env python3

__author__ = "John Giordano"
__license__ = "GPL"
__version__ = "0.7"
__maintainer__ = "John Giordano"
__status__ = "Development"

import argparse
import getpass
import json
import os
import re
import requests
from requests.auth import HTTPBasicAuth
import sys

#Variables, adjust as you need to
katello_server='https://url_for_your_katello_server'

#API Calls
activation_keys_api_call = '/katello/api/organizations/3/activation_keys?per_page=130'
content_views_api_call = '/katello/api/organizations/3/content_views?per_page=130'
hosts_api_call = '/api/organizations/3/hosts?per_page=7000'

get_activation_key_info_api_call = '/katello/api/activation_keys/'
get_content_view_info_api_call = '/katello/api/content_views/'

#We are using our own self signed certificate, no need for Python to keep telling us that.  :)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#create parser
parser = argparse.ArgumentParser(description='CLI tool for the Katello API')


#Add command line arguments
parser.add_argument('--list-act-keys', action='store_true', required=False, help='List all activation keys')
parser.add_argument('--list-cv', action='store_true', required=False, help='List all content views')
parser.add_argument('--list-cv-hosts', action='store_true',required=False, help='List all content views with all hosts attached per CV')
parser.add_argument('--list-hosts', action='store_true',required=False, help='List all hosts')
parser.add_argument('--get-act-key', required=False, help='Get info on a specific activation key.  ID is required')
parser.add_argument('--get-cv', required=False, help='Get info on a specific content view.  ID is required')
parser.add_argument('--uid', required=False, help='Username for Authentication ; Default ENV var USER')


args = (parser.parse_args())

if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

#Set Username and Password
if args.uid is None:
    your_username = os.getenv('USER')
else:
    your_username = args.uid
print("Hello \t" + your_username + "\n" )

if "KATELLO_PASSWORD" in os.environ:
    your_password = os.getenv('KATELLO_PASSWORD')
else:
    print("Password Not Found Run: \n\tread -sr KATELLO_PASSWORD\n\texport KATELLO_PASSWORD")
    exit()

#Functions

def list_act_keys(): 
   """List all Activation Keys"""

   print ("Contacting Katello API Gateway\n\n")

   get_activation_keys_request = requests.get(''.join([katello_server, activation_keys_api_call]), verify=False, auth = HTTPBasicAuth(your_username, your_password))
   #print (get_activation_keys_request.content)

   #Load up the JSON
   data_activation_keys = get_activation_keys_request.json()

   results_activation_keys = data_activation_keys['results']

   #print (type (results_activation_keys))

   get_number_of_elements_activation_keys = len (results_activation_keys)

   count = 0

   while count < get_number_of_elements_activation_keys:
      for i in results_activation_keys:
         print ("Activation Key NAME:", results_activation_keys[count]['name'])
         print ("Activation Key ID:", results_activation_keys[count]['id'])
         print ("Attached to Content View NAME:", results_activation_keys[count]['content_view']['name'])
         print ("Attached to Content View ID:", results_activation_keys[count]['content_view']['id'])
      
         print ("*******")
         count += 1

def list_cv():
   """List All Content Views"""

   print ("Contacting Katello API Gateway\n\n")

   get_content_views_request = requests.get(''.join([katello_server, content_views_api_call]), verify=False, auth = HTTPBasicAuth(your_username, your_password))
   #print (get_content_views_request.content)


   #Load up the JSON
   data_content_views = get_content_views_request.json()

   results_content_views = data_content_views['results']

   #print (type (results_content_views))

   get_number_of_elements_content_views = len (results_content_views)

   count = 0

   while count < get_number_of_elements_content_views:
      for i in results_content_views:
         print ("Content View NAME:", results_content_views[count]['name'])
         print ("Content View ID:", results_content_views[count]['id'])
      
         repositories = results_content_views[count]['repositories']
         #print ("The repositories variable is a: ", type (repositories))

         get_number_of_elements_repositories = len (repositories)

         #print ("The number of elements in the repositories list is:", get_number_of_elements_repositories)
      
         repo_count = 0

         while repo_count < get_number_of_elements_repositories:

            print ("Repository attached:", repositories[repo_count]['name'])

            repo_count += 1

         print ("*******")
         count += 1

def list_cv_hosts():
   """List all Content Views along with attached hosts"""

   print ("Contacting Katello API Gateway\n\n")

   get_content_views_verbose_request = requests.get(''.join([katello_server, content_views_api_call]), verify=False, auth = HTTPBasicAuth(your_username, your_password))
   #print (get_content_views_verbose_request.content)


   #Load up the JSON
   data_content_views_verbose = get_content_views_verbose_request.json()

   results_content_views_verbose = data_content_views_verbose['results']

   #print (type (results_content_views_verbose))

   get_number_of_elements_content_views_verbose = len (results_content_views_verbose)

   count = 0

   while count < get_number_of_elements_content_views_verbose:
      for i in results_content_views_verbose:
         print ("Content View NAME:", results_content_views_verbose[count]['name'])
         print ("Content View ID:", results_content_views_verbose[count]['id'])
      
         hosts = results_content_views_verbose[count]['hosts']
         #print ("The hosts variable is a: ", type (hosts))

         get_number_of_elements_hosts = len (hosts)

         #print ("The number of elements in the hosts list is:", get_number_of_elements_hosts)
      
         hosts_count = 0

         while hosts_count < get_number_of_elements_hosts:

            print ("Host attached:", hosts[hosts_count]['name'])

            hosts_count += 1

         print ("*******")
         count += 1

def list_hosts():   
   """List all hosts"""
   
   print ("Contacting Katello API Gateway\n\n")
   print ("This will take approximately three leisurely sips of coffee...lots of hosts/data to parse")
   

   get_hosts_request = requests.get(''.join([katello_server, hosts_api_call]), verify=False, auth = HTTPBasicAuth(your_username, your_password))
   #print (get_hosts_request.content)


   #Load up the JSON
   data_get_hosts = get_hosts_request.json()

   results_data_get_hosts = data_get_hosts['results']

   print (type (results_data_get_hosts))

   get_number_of_elements_results_data_get_hosts = len (results_data_get_hosts)

   count = 0

   while count < get_number_of_elements_results_data_get_hosts:
      for i in results_data_get_hosts:
         print ("Host NAME:", results_data_get_hosts[count]['name'])
         print ("Host ID:", results_data_get_hosts[count]['id'])
         print ("Host OS:", results_data_get_hosts[count]['operatingsystem_name'])
         print ("Host machine type", results_data_get_hosts[count]['model_name'])
         #Check if we are returning a value here
         if ('content_facet_attributes' in results_data_get_hosts[count]):
            print ("Host Content View:", results_data_get_hosts[count]['content_facet_attributes']['content_view_name'])
         #Check if we are returning a value here
         if ('subscription_facet_attributes' in results_data_get_hosts[count]):
            print ("Host Registered through:", results_data_get_hosts[count]['subscription_facet_attributes']['registered_through'])
         
         print ("*******")
         count += 1


def get_act_key(activation_key_id): 
   """Get info on a specific Activation Key"""

   print ("Contacting Katello API Gateway\n\n")

   #print ("We will be looking up Activation Key ID:", activation_key_id)

   get_activation_key_info_api_call_total = get_activation_key_info_api_call + activation_key_id

   #print ("The whole URI looks like:", get_activation_key_info_api_call_total)

   get_activation_key_info_request = requests.get(''.join([katello_server, get_activation_key_info_api_call_total]), verify=False, auth = HTTPBasicAuth(your_username, your_password))
   #print (get_activation_key_info_request.content)

   data_get_activation_key_info = get_activation_key_info_request.json()
   print (json.dumps(data_get_activation_key_info, indent=1))

def get_content_view(content_view_id): 
   """Get info on a specific Content View"""

   print ("Contacting Katello API Gateway\n\n")

   #print ("We will be looking up Content View ID:", content_view_id)

   get_content_view_info_api_call_total = get_content_view_info_api_call + content_view_id

   #print ("The whole URI looks like:", get_content_view_info_api_call_total)

   get_content_view_info_request = requests.get(''.join([katello_server, get_content_view_info_api_call_total]), verify=False, auth = HTTPBasicAuth(your_username, your_password))
   #print (get_content_view_info_request.content)

   data_get_content_view_info = get_content_view_info_request.json()
   print (json.dumps(data_get_content_view_info, indent=1))



if args.list_act_keys:

   list_act_keys()

elif args.list_cv:

   list_cv()

elif args.list_cv_hosts:

   list_cv_hosts()

elif args.list_hosts:

   list_hosts()

elif args.get_act_key:

   get_act_key(args.get_act_key)

elif args.get_cv:

   get_content_view(args.get_cv)

else:

   print ("Please specify a command line argument.  -h or --help for more info\n\n")


