import requests
import json 
from gmail_connect import ReadCredentialFile, GmailConnection #imports the lists of uid, addresses list
import sys
import time #throttle api requests
from datetime import datetime

db_file = "Deleted_Gmail_Spam.db"

#read in Abstract API credentials from file location
def ReadAbstractCred():
    file_path = r"C:\Users\jsbay\OneDrive - Auburn University\ISMN COURSES\DevTools\Credentials\abstractCred_temp.json"
    try:
        with open(file_path, "r") as file:
            abstract_cred = json.load(file)
        return abstract_cred
    except FileNotFoundError:
        print("Cannot find the file to authenticate with Abstract API. Exiting program.")  
#(enhancement) *is there a way to get a device notification if a process fails while running the script? Research*
        sys.exit()

def AbstractAPICall(abstract_cred, addresses):
    endpoint = "https://emailvalidation.abstractapi.com/v1/"
    query_dict = {
        "api_key": abstract_cred["api_key"],
    }
    api_json = []
    for addr in addresses: #addresses is from the list of addr in gmail_connect module
        query_dict["email"] = addr #each email will be placed in this dictionary location
        query_dict["auto_correct"] = False #will keep each email the same as what is currently in the inbox (open Abstract documentation)
        response = requests.get(endpoint, params=query_dict)
        if(response.status_code == 200):
            data = response.json()
            api_json.append(data)
            time.sleep(1/3) #change the rate of calls per second once a new api key is issued  
        else:
            print(f"{response.status_code} {response.reason}. Exiting.")
            sys.exit()
    with open('EmailList.json', 'w') as emailFile:
        json.dump(api_json, emailFile, indent=4)
        print("Done. All email address json data is located in the 'EmailList.json' file.")

# perform analysis on data retrieved from API call
def APIAnalysis():
    trash_email = []
    with open('EmailList.json', "r") as email_file: 
        api_json = json.load(email_file)
    for data in api_json:
        email = data["email"]
        quality_score = float(data["quality_score"]) #type casting from string to float
        is_mx_found = bool(data["is_mx_found"]["value"])
        is_smtp_valid = bool(data["is_smtp_valid"]["value"])
        if(quality_score <= 0.4 or is_mx_found == False or is_smtp_valid == False):
            trash_email.append(email)
    print("Analysis is complete.")
    return trash_email #return to gmail_delete.py file (to the function that calls it)

def TrashAnalysis(trash_email):
    if(len(trash_email) == 0): #if length of trash_email list is empty
        #("There are no emails to analyze!")
        subject = "Trash Mail Report" #build the subject/body to send an email report of findings
        report_file = "Trash_Gmail_Report.txt"
        body = "" #initialize to empty string
        with open(report_file, "w") as report:
            email_body = f"\nTrashed Emails - {datetime.now()}\nThere were no emails to analyze for spam."
            report.write(email_body)
            body += email_body
        from gmail_delete import SendReportEmail #import module to send report email
        SendReportEmail(subject, report_file, credentials, body)
        sys.exit()
    else:
        from gmail_delete import MoveToTrash #else, move the emails in trash_email using MoveToTrash module
        MoveToTrash(credentials, db_file,trash_email)
        print("Done! Make sure to check files and email for updates.")
        sys.exit()
    #check to make sure there is actually a list of emails to put in trash, if so, call MoveToTrash()

credentials = ReadCredentialFile()
uid, addresses = GmailConnection(credentials) #lists of uid and addresses
abstract_cred = ReadAbstractCred()
api_json =  AbstractAPICall(abstract_cred, addresses) #list of json data
trash_email = APIAnalysis()
TrashAnalysis(trash_email)