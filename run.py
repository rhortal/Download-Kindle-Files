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
from call_rclone import call_rclone
class Email:
    def __init__(self, subject, html_content):
        self.subject = subject
        self.html_content = html_content
        self.links = self.extract_links()

    def extract_links(self):
        #Extracts all links from the HTML content.
        soup = BeautifulSoup(self.html_content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]
    
    def filename(self):
        #Creates a string-safe filename to use for saving
        start = self.subject.find('\"') + 1  # +1 to exclude the first quote
        end = self.subject.find('\"', start)  # Find the next quote after the start
        return self.subject[start:end].replace('/', '-')
        
load_dotenv()

# IMAP server settings
IMAP_SERVER = os.getenv('IMAP_SERVER', 'imap.gmail.com')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
APP_PASSWORD = os.getenv('APP_PASSWORD')
ATTACHMENT_PATH = os.getenv('ATTACHMENT_PATH', 'attachments') # path to save attachments in the current directory.

# How many days back?
DAYS_BACK = os.getenv('DAYS_BACK', '7') # Default to one week. Links expire in 7 days

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

"""     if TESTING:
        print("Test output")
        # Print the subjects of the fetched emails
        for msg in fetched_emails:
            print(msg.subject)  # Print the subject of each fetched email
        
        # Exit after printing subjects if needed for testing purposes
        exit()
"""
    # Process the bodies of the fetched emails normally
emails = []
for msg in fetched_emails:
    email = Email(subject=msg.subject, html_content=msg.html)
    emails.append(email) 

if TESTING:
    # Example: Printing the email records
    for email in emails:
        print(f"Subject: {email.subject}")
        print(f"Links: {email.links}")
        print(f"Filename: {email.filename()}")
        print()
    exit()


print("Downloading from " + str(len(emails)) + " messages")

for email in emails:
    index = 0
    for link in email.extract_links():
        if index == 2:
                continue
        extension = ".txt" if index % 3 == 0 else ".pdf"
        filename = email.filename() + extension # os.path.basename(result)  
        file_path = f'{ATTACHMENT_PATH}/{filename}'
        if os.path.isfile(file_path):
            print (filename + " already exists")
            continue
        print ("Downloading "+ filename)
        resp = requests.get(link)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        output = open(f'{ATTACHMENT_PATH}/{filename}' , 'wb')
        output.write(resp.content)
        output.close()
        print ("Downloaded "+ filename)
        index += 1   # Increase the counter for each downloaded file.

RCLONE = os.getenv('RCLONE')
if RCLONE: # If rclone is set, upload to cloud storage using it...
    RCLONE_PATH = os.getenv('RCLONE_PATH')
    # use rclone to copy files to cloud 
    call_rclone('copy', ATTACHMENT_PATH + ' ' + RCLONE_PATH)

# print ("All done!")