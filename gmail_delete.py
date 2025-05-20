from imap_tools import MailBox
from gmail_connect import GmailConnection
import sqlite3
from datetime import datetime
#import smtp protocol libraries to send an email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
import json

db_file = "Deleted_Gmail_Spam.db"

#read in email credentials again to move emails from spam to trash
def CredentialFile():
    file_path = r"C:\Users\jsbay\OneDrive - Auburn University\ISMN COURSES\DevTools\Credentials\gmailCred.json"
    try:
        with open(file_path, "r") as file:
            credentials = json.load(file)
        return credentials
    except FileNotFoundError:
        print("Cannot find the file to authenticate with IMAP Servers. Exiting program.")
        sys.exit()

def SendReportEmail(subject, report_file, credentials, body): #used in Question1.py to send emails and accepts different arguments
    credentials = CredentialFile()
    sender_email = credentials["user"]
    recipient_email = sender_email
    password = credentials["app_password"] 

    #Create email
    msg = MIMEMultipart() # msg can contain multiple types (text, attachments)
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach the error file
    with open(report_file, "rb") as file: #open report_file in binary read mode (currently empty, will be filled with error content later in code)
        part = MIMEBase("application", "octet-stream") #specify part as binary stream
        part.set_payload(file.read())  #read and set the content of the file as the payload
        encoders.encode_base64(part) #encode the payload in Base64
        part.add_header(
            "Content-Disposition",  # Set the header for file attachment
            f"attachment; filename={os.path.basename(report_file)}",  # Specify the file's name in the attachment
        )
        msg.attach(part) #attach the file to the email object

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server: #connect to gmail SMTP server on secure port 587
            server.starttls() #start transport layer security encryption to encrypt communication between client and server
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Error email sent successfully.")
    except Exception as e:
        print(f"Failed to send error email: {e}")
        sys.exit()

def CreateDB(db_file):
    if(not os.path.exists(db_file)): #will bypass if db_file already exists
        dbConn = sqlite3.connect(db_file)
        cursor = dbConn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS spam_emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid INTEGER UNIQUE,
        email_address TEXT,
        date TEXT 
        )""")
        dbConn.commit()
        dbConn.close()

def MoveToTrash(credentials, db_file, trash_emailList): #must authenticate with gmail credentials to move mail
    credentials = CredentialFile()
    uidList, addrList = GmailConnection(credentials)  #list of uids and list of addresses from gmail junk inbox
    imap_url = "imap.gmail.com"
    user, password = credentials["user"], credentials["app_password"]
    CreateDB(db_file) #call create Db if it does not exist on disk, will bypass if db_file already exists
    with MailBox(imap_url).login(user, password) as mb:
        reportList = []
        mb.folder.set("[Gmail]/Spam")
        for addr in trash_emailList: 
            uid = None #if uid is null for some reason (should not be)
            if addr in addrList: #if addr in trash_emailList == an original email value(if an email that met trash criteria == an email scraped from spam folder)
                try:
                    uid = uidList[addrList.index(addr)] #get the uid for the corresponding addr index to move the email to trash based on its UID, not its email address
                    dbConn = sqlite3.connect(db_file)
                    cursor = dbConn.cursor()
                    cursor.execute(f"""INSERT INTO spam_emails (uid, email_address, date)
                    VALUES (?, ?, datetime('now'))""", (uid, addr))
                    dbConn.commit()
                    dbConn.close()
                    mb.move(uid,"[Gmail]/Trash") #move the email with the specific uid into the trash folder
                    report_emails = {
                    "uid": uid,
                    "email_address": addr
                    }
                    reportList.append(report_emails)
                except sqlite3.DatabaseError as e: #keep a file that tracks error
                    report_file = "DB_Error.txt"
                    with open(report_file, "a") as email_e_file:
                        subject = "Database Error Notification"
                        body = f"Error occurred: ({e}) while committing spam emails to Deleted_Gmail_Spam.db - {datetime.now()}\nuid = {uid}\nemail_address = {addr}\n"
                        email_e_file.write(body)
                        SendReportEmail(subject, report_file, credentials, body)
                    raise
    subject = "Trash Mail Report"
    report_file = "Trash_Gmail_Report.txt"
    body = ""
    with open(report_file, "w") as report:
        report.write(f"\nTrashed Emails - {datetime.now()}\n")
        for email in reportList:
            email_body = f"{email['uid']}\n{email['email_address']}\n"
            report.write(email_body)
            body += email_body
    SendReportEmail(subject, report_file, credentials, body)