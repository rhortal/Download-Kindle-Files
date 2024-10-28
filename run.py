#!/usr/bin/env python3

from imap_tools import MailBox
from imap_tools import AND, OR, NOT
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
import re
from pathlib import Path

load_dotenv()

# IMAP server settings
IMAP_SERVER = os.getenv('IMAP_SERVER', 'imap.gmail.com')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
APP_PASSWORD = os.getenv('APP_PASSWORD')
ATTACHMENT_PATH = os.getenv('ATTACHMENT_PATH', 'attachments') # path to save attachments in the current directory.

# How many days back?
DAYS_BACK = os.getenv('DAYS_BACK', '10')

# Calculate the date range for today and yesterday
today = datetime.now()
yesterday = today - timedelta(days=int(DAYS_BACK))

# Format dates for the IMAP query (you can adjust the format as needed)
today_str = today.strftime('%d-%b-%Y')
yesterday_str = yesterday.strftime('%d-%b-%Y')

# Set TESTING variable
TESTING = False  # Set to False when you want to run your actual email fetching code

# get list of email bodies from INBOX folder
with MailBox(IMAP_SERVER).login(EMAIL_ADDRESS, APP_PASSWORD, 'INBOX') as mailbox:
    # Fetch emails with the subject filter, even in testing mode
    fetched_emails = [
        msg for msg in mailbox.fetch(
            AND(
                subject='from your Kindle',  # Use wildcard for NAME
                # seen=False,  # Fetch only unread emails
                date_gte=datetime.date(yesterday)  # Initially filter for yesterday's emails
            ),
            reverse=True
        )
    ]

    if TESTING:
        print("Test output")
        # Print the subjects of the fetched emails
        for msg in fetched_emails:
            print(msg.subject)  # Print the subject of each fetched email
        
        # Exit after printing subjects if needed for testing purposes
        exit()

    # Process the bodies of the fetched emails normally
    bodies = [msg.html for msg in fetched_emails]
   
# Extract URLs
soup = BeautifulSoup(str(bodies),features="html.parser")
links = []
for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
    links.append(link.get('href'))

# Delete every third link, only the first 2 of each message are valid
""" while links:
    for index in reversed(range(2, len(links), 3)):
        del links[index]# Best replace this with something that looks for the right string on the URL
        print ('deleted link ' + str(index)) """

index = 0
for result in links:
    print ('Geting ' + result)
    resp = requests.get(result)
    filename = "attachment" + str(index) + ".pdf" # os.path.basename(result)
    print (filename)
    os.makedirs(os.path.dirname(f'{ATTACHMENT_PATH}/{filename}'), exist_ok=True)
    output = open(f'{ATTACHMENT_PATH}/{filename}' , 'wb')
    output.write(resp.content)
    output.close()
    index += 1   # Increase the counter for each downloaded file (PDFs are saved in separate files with incrementing names). This is to avoid overwriting existing PDF's when we start downloading again from scratch, which would be a waste of time. Also it will make sure that all pdf attachments get stored separately and not mixed together

print ('All done!')