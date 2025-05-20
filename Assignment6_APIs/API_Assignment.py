import requests
import sys
import re
import json
import os
import random

def CheckAPIKey(): #make sure there is an API key in the scope of the program
    try:
        api_key = os.environ.get('ISMNAPIKEY') #mask the api_key in an environment variable on os
    except:
        if api_key is None: #if the api_key does not hold a value from os.environ.get()
            ApiMetaData(api_key) #401 error is what will occur
    return api_key

def Strip_HTML_Tags(text): #remove HTML tags from response errors to display to the console
    clean_text = re.sub('<.*?>', '', text)
    return clean_text

def ApiMetaData(api_key):
    header = {} #declare header as a dictionary to hold api key in header
    header["x-api-key"] = api_key
    endpoint = "https://ismn5650-questionsapi.azurewebsites.net/metadata"
    response = requests.get(endpoint, headers=header) #pass endpoint, query string, request headers
    if(response.status_code in (401, 403)):
        data = response.json() #message is stored in json
        print(f"""{data["message"]}. You must authenticate and request a key from this link: (https://ismn-assignment-checker.azurewebsites.net/genkey
Make sure to insert your key into a recognizable OS location for the program to run.""") #print the message value from the message dictionary
        sys.exit()

def ApiErrors(response): #print errors connecting to API
    if response.status_code != 200:
        try:
            #attempt to get error details from response JSON
            error_details = response.json().get('error', response.text)
        except ValueError:
            #if response is not JSON, use plain text or a generic message
            error_details = Strip_HTML_Tags(response.text)
        print(f"Error occurred: {response.status_code}. {error_details}. Exiting program.")
        sys.exit()
        
def Option1(api_key):
    header = {} #declare header as a dictionary to hold api key in header
    header["x-api-key"] = api_key
    endpoint = "https://ismn5650-questionsapi.azurewebsites.net/stats"
    response = requests.get(endpoint, headers=header) #pass endpoint, query string, request headers
    if(response.status_code == 200):
        data = response.json()
        with open('stats.json', "w") as json_file:
            json.dump(data, json_file, indent=4) #dump json into a file 

        for d in data:
            category = d["category"]
            print(f"{category["id"]}) {category["name"]}")

        print()
        valid_cat_ID = False
        while(valid_cat_ID != True):
            value = input("Choose a category ID: ")
            print()
            for d in data:
                category = d["category"]
                if str(category["id"]) == value:
                    print(f"{category["name"]} Details: ")
                    print()
                    PrintStats(d, "easy")
                    PrintStats(d, "medium")
                    PrintStats(d, "hard")
                    valid_cat_ID = True
                    break
            if(valid_cat_ID == False):
                print("Invalid category ID. Please try again.")
    else:
        if(response.status_code in (401, 403)): #unauthorized or forbidden
            ApiMetaData(api_key)
        else: #other errors not handled by meta get response
            ApiErrors(response)

def Option2(api_key): 
    header = {} #declare header as a dictionary to hold api key in header
    header["x-api-key"] = api_key
    stats_endpoint = "https://ismn5650-questionsapi.azurewebsites.net/stats"
    response = requests.get(stats_endpoint, headers=header) #pass endpoint, query string, request headers
    if(response.status_code == 200):
        categoryList = response.json()
    else:
        if(response.status_code in (401, 403)): #unauthorized or forbidden (sys.exit())
            ApiMetaData(api_key)
        else: #other errors not handled by meta get response (sys.exit())
            ApiErrors(response)
    for c in categoryList:
        category = c["category"]
        print(f"{category["id"]}) {category["name"]}")
    print()
    valid_cat_ID = False
    while(valid_cat_ID != True):
        cid = input("Choose a category ID: ")
        for c in categoryList:
            category = c["category"]
            if str(category["id"]) == cid:
                valid_cat_ID = True
                selected_category = c #this will hold one single dictionary from the ID entered
                break
        if(valid_cat_ID == False):
            print("Invalid category ID. Please try again.")
    print()
    valid_diff_level = False
    while(valid_diff_level != True):
        print("""1. Easy
2. Medium
3. Hard""")
        print()
        diff_level = int(input("Choose a difficulty level (1, 2, 3): "))
        if(diff_level not in (1,2,3)):
            print("Invalid difficulty level entry. Please enter 1, 2, or 3.")
            valid_diff_level = False
            continue
        else:
            valid_diff_level = True
            if(diff_level == 1):
                d = "easy"
            elif(diff_level == 2):
                d = "medium"
            elif(diff_level == 3):
                d = "hard"
            difficulty_data = selected_category.get(d, {}) #get the specified difficulty's dictionary within the user's selected category dictionary
            if (difficulty_data.get("boolean", 0) == 0 and difficulty_data.get("multiple", 0) == 0):
                print("There are no trivia questions available for this difficulty level. Please select a different difficulty level.")
                valid_diff_level = False
                continue
            else:
                valid_diff_level = True  #exit loop if valid difficulty with questions
                break
    params_dict = {
        "cid": cid,  #category ID
        "d": d       #difficulty level
    }
#pass cid, d, and api-key into query string in order to retrive the category and difficulty of the questions
    questions_endpoint = "https://ismn5650-questionsapi.azurewebsites.net/questions"
    response = requests.get(questions_endpoint, params=params_dict, headers=header)
    if(response.status_code == 200):
        questionsList = response.json()  
        with open("questions.json", "w") as question_file: #this is just for my analysis 
            json.dump(questionsList, question_file, indent=4)
        
        score = 0 #track how many answers the user gets correct
        for q in questionsList:
            questions = [] #set to an empty list for each iteration
            incorrect_ans = []
            correct_ans = [] #keep separate to know what the correct answer is
            answer_choices = []
            questions.append(q["question"])
            for inc_answers in q["incorrect_answers"]:
                incorrect_ans.append(inc_answers)
            correct_ans.append(q["correct_answer"])
            answer_choices = incorrect_ans + correct_ans #concatenate two lists into total answer choices
            random.shuffle(answer_choices) #built in shuffle function imported from the random module in python
            correct_answer = q["correct_answer"]
            question = q["question"]
            print()
            choice_incrementer = 1
            print(f"Question: {question}")
            print()
            for choice in answer_choices:
                print(f"{choice_incrementer}) {choice}")
                choice_incrementer += 1
            validAnswer_num = False
            while (validAnswer_num != True):
                user_numAnswer = input("Enter the number of your answer: ").strip()
                # Check for empty input
                if user_numAnswer == '':
                    print("Please enter a number value.")
                    continue
                try:
                    user_numAnswer = int(user_numAnswer)
                    validAnswer_num = True  #exit loop if conversion is successful
                except ValueError:
                    print("Enter a valid integer value.")
                    validAnswer_num = False
                    continue
                if (1 <= int(user_numAnswer) <= len(answer_choices)):
                    validAnswer_num = True
                    user_numAnswer = int(user_numAnswer - 1) #lists index at 0 
                    user_valueAnswer = answer_choices[user_numAnswer]
                    if(user_valueAnswer == correct_answer):
                        print("Correct!")
                        score += 1
                    else:
                        print(f"""Incorrect.                
The correct answer is {correct_answer}.""")
                else:
                    print("Invalid answer option. Please try again.")
                    validAnswer_num = False
        print()
        percentage = score/len(questionsList) * 100
        print(f"Final Score: {score}/{len(questionsList)} = {percentage}%")
    else:
        if(response.status_code in (401, 403)): #unauthorized or forbidden (sys.exit())
            ApiMetaData(api_key)
        else: #other errors not handled by meta get response (sys.exit())
            ApiErrors(response)

def PrintStats(stat, difftype):
    print(f"Question Difficulty: {difftype}".title())
    typedict = stat[difftype] #stat is category dictionary from Option1 function
    print(f"T/F = {typedict["boolean"]}")
    print(f"Multiple = {typedict["multiple"]}")

def MenuOption():
    print("""Welcome to Trivia Game!
1. Lookup Category Statistics
2. Play Trivia Game
3. Exit""")
    menuOption = int(input("Choose your menu option: "))
    return menuOption

def Main(): #control the flow of the program
    exitProgram = False
    while(exitProgram != True):
        print()
        menuOption = MenuOption()
        api_key = CheckAPIKey()
        match menuOption:
            case 1:
                print()
                Option1(api_key) #returns the list of data from Option1
            case 2:
                print()
                Option2(api_key)
            case 3:
                print("Thanks for playing. Goodbye!")
                exitProgram = True
            case _: #default case
                print("Invalid menu option. Please choose option 1, 2, or 3.")
Main()