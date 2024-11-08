#!/usr/bin/env python3

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from imap_tools import MailBox, AND
from call_rclone import call_rclone
from classEmail import Email

def load_environment_variables():
    load_dotenv()
    return {
        "IMAP_SERVER": os.getenv('IMAP_SERVER', 'imap.gmail.com'),
        "EMAIL_ADDRESS": os.getenv('EMAIL_ADDRESS'),
        "APP_PASSWORD": os.getenv('APP_PASSWORD'),
        "ATTACHMENT_PATH": os.getenv('ATTACHMENT_PATH', 'attachments'),
        "DAYS_BACK": int(os.getenv('DAYS_BACK', '7')),
        "RCLONE": os.getenv('RCLONE'),
        "RCLONE_PATH": os.getenv('RCLONE_PATH')
    }

def fetch_emails(imap_server, email_address, app_password, days_back):
    today = datetime.now()
    yesterday = today - timedelta(days=days_back)

    with MailBox(imap_server).login(email_address, app_password, 'INBOX') as mailbox:
        fetched_emails = [
            msg for msg in mailbox.fetch(
                AND(
                    subject='from your Kindle', 
                    date_gte=yesterday.date()
                ),
                reverse=True
            )
        ]
    return fetched_emails

def process_emails(fetched_emails):
    emails = []
    for msg in fetched_emails:
        email = Email(subject=msg.subject, html_content=msg.html)
        emails.append(email)
    return emails

def download_links(emails, attachment_path):
    print("Downloading from " + str(len(emails)) + " messages")
    for email in emails:
        index = 0
        for link in email.extract_links():
            if index == 2:
                continue
            extension = ".txt" if index % 3 == 0 else ".pdf"
            filename = email.filename() + extension  
            file_path = os.path.join(attachment_path, filename)
            if os.path.isfile(file_path):
                print(filename + " already exists")
                continue
            print("Downloading " + filename)
            resp = requests.get(link)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as output:
                output.write(resp.content)
            print("Downloaded " + filename)
            index += 1  

def upload_to_cloud(rclone, attachment_path, rclone_path):
    if rclone:
        call_rclone('copy', attachment_path, rclone_path)

def main():
    env_vars = load_environment_variables()
    imap_server = env_vars['IMAP_SERVER']
    email_address = env_vars['EMAIL_ADDRESS']
    app_password = env_vars['APP_PASSWORD']
    attachment_path = env_vars['ATTACHMENT_PATH']
    days_back = env_vars['DAYS_BACK']
    rclone = env_vars['RCLONE']
    rclone_path = env_vars['RCLONE_PATH']

    fetched_emails = fetch_emails(imap_server, email_address, app_password, days_back)
    emails = process_emails(fetched_emails)
    
    download_links(emails, attachment_path)
    upload_to_cloud(rclone, attachment_path, rclone_path)

if __name__ == '__main__':
    main()
