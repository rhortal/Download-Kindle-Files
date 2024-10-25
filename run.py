#!/usr/bin/env python3

from imap_tools import MailBox
from imap_tools import AND, OR, NOT
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse

load_dotenv()

# IMAP server settings
IMAP_SERVER = os.getenv('IMAP_SERVER'', 'imap.gmail.com')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
APP_PASSWORD = os.getenv('APP_PASSWORD')
ATTACHMENT_PATH = os.getenv('ATTACHMENT_PATH', 'attachments') # path to save attachments in the current directory.

# get list of email bodies from INBOX folder
with MailBox(IMAP_SERVER).login(EMAIL_ADDRESS, APP_PASSWORD, 'INBOX') as mailbox:
    bodies = [msg.html for msg in mailbox.fetch(AND(subject='your email subject'), reverse = True)]
   
# Extract URLs
soup = BeautifulSoup(str(bodies))
links = []
for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
    links.append(link.get('href'))

# Delete every third link, only the first 2 of each message are valid
while links: [del links[index] for index in reversed(range(2, len(my_list), 3))]
# Best replace this with something that looks for the right string on the URL

for result in links:    
    resp = requests.get(result)
    filename = os.path.basename(result.path)
    output = open(f'{ATTACHMENT_PATH}/{filename}' , 'wb')
    output.write(resp.content)
    output.close()

print ('All done!')