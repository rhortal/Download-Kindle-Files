#!/usr/bin/env python3

from imap_tools import MailBox
from imap_tools import AND, OR, NOT
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# IMAP server settings
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
APP_PASSWORD = os.getenv('APP_PASSWORD')

# get list of email bodies from INBOX folder
with MailBox($IMAP_SERVER).login($EMAIL_ADDRESS, $APP_PASSWORD, 'INBOX') as mailbox:
    bodies = [msg.html for msg in mailbox.fetch(AND(subject='your email subject'), reverse = True)]
   

soup = BeautifulSoup(str(bodies))
links = []
for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
    links.append(link.get('href'))
links # in this you will have to check the link number starting from 0. 

result = links[5] # mine was 5th
result

resp = requests.get(result)

output = open('test.csv', 'wb')
output.write(resp.content)
output.close()