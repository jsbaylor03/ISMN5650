from imap_tools import MailBox
import json
import sys

#had to allow imap settings for gmail and create an app password

#read in file that has gmail credentials to connect to my gmail through imap google servers
def ReadCredentialFile():
    file_path = r"C:\Users\jsbay\OneDrive - Auburn University\ISMN COURSES\DevTools\Credentials\gmailCred.json"
    try:
        with open(file_path, "r") as file:
            credentials = json.load(file)
        return credentials
    except FileNotFoundError:
        print("Cannot find the file to authenticate with IMAP Servers. Exiting program.")
        sys.exit() #exit program if there are no google credentials to read in

#connect to incoming google mail server requires SSL for encrypted communication of credentials on port 993 (imap_tools library handles this)
def GmailConnection(credentials):
    imap_url = "imap.gmail.com" 
    user, password = credentials["user"], credentials["app_password"]

    uid = [] #get the unique id of the message
    addresses = [] #get the list of addresses in spam folder
    seen_addr = set()

    #read in database field uid, make sure no emails that are already seen_addr get filtered out 
    #(enhancements)make sure to print/add the date the email was sent to the database entry and emails in db get filtered out

    with MailBox(imap_url).login(user, password) as mb:
        mb.folder.set("[Gmail]/Spam")  #set to Gmail's IMAP Spam folder
        for msg in mb.fetch(limit=50, reverse=True, mark_seen=False): #fetch senders from spam folder (will be less than limit if emails are already in seen_addr)
            if msg.from_ not in seen_addr:
                print("From:", msg.from_) #just for me to see in the terminal
                seen_addr.add(msg.from_) #add addr into seen_addr
                uid.append(msg.uid) #append each uid into the uid list to use later for deletion
                addresses.append(msg.from_)
    return uid, addresses

