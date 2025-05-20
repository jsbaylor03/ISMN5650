import json
import os

exitProgram = False #or exitProgram = 5 (The last menu item)
var = """ 
    1. Add a book
    2. Display all books
    3. Search for a book by title
    4. Update book status
    5. Remove book from library
    6. Exit Program
    """
#used for exiting a loop/if user wants to continue with action
yes = "Y"
no = "N"
lib_jsonFile = [] #this will hold the library data for the program to access freely/make changes during runtime
bookFile = "Book_Library.json"

if(os.path.exists(bookFile)): #checks if the file exists, if not, create the file with an empty list 
    if(os.path.getsize(bookFile) > 0): #checks if there are contents in the bookFile
        with open(bookFile, "r") as bookLibrary:
            lib_jsonFile = json.load(bookLibrary) #load/read in file to lib_jsonFile list if there are contents inside 
else: #will really only execute if the bookFile does not exist
    lib_jsonFile = []

# Dictionary/list declarations above while loop

while(exitProgram != True):
    print("Welcome to the Library Book Tracker!")
    validChoice = False

    #input check for menu options
    while(validChoice != True): #entry to choosing a menu option
        print(var) #print the menu each loop iteration
        userChoice = input("Choose a menu option: ")
        userChoice = int(userChoice) #simply for condensing validation
        if(userChoice < 1 or userChoice > 6):
            print("Invalid menu option. Please enter an option between 1-6.")
            validChoice = False
        else:
            validChoice = True
    
    if(userChoice == 1):
        addBook = True
        while(addBook != False):
            bookDict = {}
            
            inputTitle = input("Enter book title: ")
            inputAuthor = input("Enter book author: ")
            inputStatus = input("Enter book status (Available/Checked Out) *Case Sensitive*: ")

            while(inputStatus != "Available" and inputStatus != "Checked Out"):
                print("Invalid input.")
                inputStatus = input("Please enter valid status (Available/Checked Out) *Case Sensitive*: ")

            #create a key value pair for bookDict dictionary 
            bookDict["Title"] = inputTitle
            bookDict["Author"] = inputAuthor
            bookDict["Status"] = inputStatus

            #append each dictionary entry to the list
            lib_jsonFile.append(bookDict) #append bookDict to jsonFile, THEN write changes to file

            with open(bookFile, 'w') as bookLibrary:  #dump lib_jsonFile all into bookFile
                json.dump(lib_jsonFile, bookLibrary, indent = 4)
            
            print("Book added successfully!")
            addBooks = False #for repeating outer loop to add multiple books + input validation

            while(addBooks != True):
                endAddBook = input("Would you like to add another book? Type Y/N: ")
                #add lower() function to endAddBook
                if(endAddBook.lower() == yes.lower()):
                    addBook = True
                    addBooks = True #should return to outer loop to add more books
                elif(endAddBook.lower() == no.lower()):
                    addBook = False #exit outer loop
                    addBooks = True #set to true to exit inner while
                    print("Done!")
                else:
                    print("Invalid input.")
                    print()
                    addBooks = False #prompts user to type Y/N again at the top of loop


    if(userChoice == 2):
        print("Books in the library: \n")
        #Display books like "Harry Potter by J.K. Rowling (Available)" with a new line for each dictionary book entry
            
        bookIncrementer = 0 #displays books with a number in front
        for b in lib_jsonFile:
            strBook = b["Title"]
            strAuthor = b["Author"]
            strStatus = b["Status"]
            bookIncrementer += 1
            print(f"{bookIncrementer}. '{strBook}' by {strAuthor} ({strStatus}) \n") #keep inside for loop to print each dictionary entry

    if(userChoice == 3):
        continueSearch = True

        while(continueSearch != False):
            searchedBook = input("Enter the title of the book to search: ")
            bookFound = False

            for b in lib_jsonFile:
                if(b["Title"].lower() == searchedBook.lower()):
                    strBook = b["Title"]
                    strAuthor = b["Author"]
                    strStatus = b["Status"]
                    print(f"Book Found: \n'{strBook}' by {strAuthor} ({strStatus}) \n")
                    bookFound = True
            if(bookFound != True):  
                print(f"'{searchedBook}' was not found in the library.")
                
            validSearchOpt = False
            
            while(validSearchOpt != True):
                searchInput = input("Would you like to search another book? Y/N: ")
                if(searchInput.lower() == yes.lower()):
                    continueSearch = True
                    validSearchOpt = True
                elif(searchInput.lower() == no.lower()):
                    continueSearch = False
                    validSearchOpt = True
                    print("Book Search complete!")
                else:
                    print("Invalid input. \n")
                    continueSearch == True
                    validSearchOpt = False

    if(userChoice == 4):
        continueUpdate = True
        
        while(continueUpdate != False):
            updateBook = input("Enter the title of the book to update: ")
            bookFound = False
            
            for b in lib_jsonFile:
                if(b["Title"].lower() == updateBook.lower()):
                    newStatus = input("Enter new status (Available/Checked Out) *Case Sensitive*: ")
                    bookFound = True

                    while(newStatus != "Available" and newStatus!= "Checked Out"):
                        print("Invalid input.")
                        newStatus = input("Please enter valid status (Available/Checked Out): ")

                    #checks to see if the status input by the user already matches the book's library status
                    if(b["Status"] == newStatus):
                        print("The book's current status matches your status input.")
                    else:
                        b["Status"] = newStatus
                        with open(bookFile, 'w') as bookLibrary: #updates the status changed
                            json.dump(lib_jsonFile, bookLibrary, indent = 4)
                        print("Book status updated!")
            if(bookFound != True): #book was not found in for loop
                print(f"'{updateBook}' was not found in the library")
            
            validUpdateOpt = False
            while(validUpdateOpt != True):
                updateInput = input("Would you like to update another book? Y/N: ")
                if(updateInput.lower() == yes.lower()):
                    validUpdateOpt = True
                    continueUpdate = True
                elif(updateInput.lower() == no.lower()):
                    validUpdateOpt = True
                    continueUpdate = False
                    print("Done!")
                else:
                    print("Invalid input. \n")
                    validUpdateOpt = False
                    continueUpdate = True

    if(userChoice == 5):
        #remove the book from library based on title (search for valid title)
        continueRemove = True
        
        while(continueRemove != False):
            removeBook = input("Enter the title of the book to remove: ")
            bookFound = False
            for b in lib_jsonFile:
                if(b["Title"].lower() == removeBook.lower()):
                    lib_jsonFile.remove(b)
                    with open(bookFile, "w") as bookLibrary: #writes the new changes/removals into the bookFile
                        json.dump(lib_jsonFile, bookLibrary, indent = 4)
                    print(f"Removed '{removeBook}' from the JSON file.")
                    bookFound = True
            if(bookFound != True):
                print(f"'{removeBook}' cannot be removed because it is not in the {bookFile} file.")
            
            validRemoveOpt = False
            while(validRemoveOpt != True):
                removeInput = input("Would you like to remove another book? Y/N: ")
                if(removeInput.lower() == yes.lower()):
                    validRemoveOpt = True
                    continueRemove = True
                elif(removeInput.lower() == no.lower()):
                    validRemoveOpt = True
                    continueRemove = False
                    print("Done!")
                else:
                    print("Invalid input. \n")
                    validRemoveOpt = False
                    continueRemove = True

    if(userChoice == 6):
        print(f"You can find the current library in this file: {bookFile}.")
        print("Thank you for visiting the library. Goodbye!")
        exitProgram = True