import sqlite3
import sys
import datetime 

def GetCustomer(name):
    try:
        dbconnection = sqlite3.connect('Assignment5.db')
        cursor = dbconnection.cursor()
        cursor.execute("select id, name, date_of_birth, contact_info, address from customers") #returns all rows from customers table
        customerData = cursor.fetchall() #customerData is a list
        dbconnection.close()

        customerID = 0
        for customer in customerData: #customer[1] is the name
            if(customer[1].title() == name):
                customerID = customer[0] #receive the ID of the customer's name
                return customerID #return customerID
        return customerID #return ID 0 if this exits the for loop without an ID
    except:
        print("Cannot execute program without database file in scope. Exiting program.")
        sys.exit() #gracefully exit program

def InsertCustomer(name):
    customerID = GetCustomer(name)
    validDOB = False
    validPhone = False
    if(customerID != 0): #customer was found in the database
        return customerID #return to InsertDrugs customerID variable & bypass proceeding code
    else:
        customerList = []
        customerList.append(name)
        
        while(validDOB != True): #DOB must have a yyyy-mm-dd format to limit database field formatting issues
            dob = input("Enter your DOB (yyyy-mm-dd): ")
        # Check length and slashes
            if (len(dob) == 10 and dob[4] == '-' and dob[7] == '-'):
                try: 
                    #store the m,d,y as numbers to be tested for validity
                    month = int(dob[5:7])
                    day = int(dob[8:])
                    year = int(dob[:4])
                
                    if (1 <= month <= 12 and 1900 <= year <= 2100): #valid range
                        if (month in [4, 6, 9, 11] and not (1 <= day <= 30)): #april, june, sept, nov.
                            print(f"Invalid day entry for this month. Please enter a day between 1 and 30.")
                            validDOB = False
                        elif(month in [1,3,5,7,8,10,12] and not (1 <= day <= 31)): 
                            print(f"Invalid day entry for month. Please enter a day between 1 and 31.")
                            validDOB = False
                        elif(month == 2 and not (1 <= day <= 28)): #does not account for leap year
                            print(f"Invalid day entry for February. Please enter a day between 1 and 28.")
                            validDOB = False
                        else:
                            validDOB = True
                            customerList.append(dob)
                    else:
                        print(f"Invalid month/year entry.")
                        validDOB = False
                except:
                    print("Invalid date format. Please use yyyy-mm-dd.")
                    validDOB = False
                    continue  #continue to the next iteration if there's an invalid conversion
            else:
                print("Invalid date format. Please enter yyyy-mm-dd")
                validDOB = False
        
        # Validate phone number
        while(validPhone != True):
            phoneNum = input("Enter your phone number ###-###-####: ")
            if (len(phoneNum) == 12 and phoneNum[3] == '-' and phoneNum[7] == '-'):
                if(phoneNum[:3].isnumeric() and phoneNum[4:7].isnumeric() and phoneNum[8:].isnumeric()):
                    customerList.append(phoneNum)
                    validPhone = True
                else:
                    print("Invalid phone number. Please enter ###-###-####.")
            else:
                print("Invalid phone number. Please enter ###-###-####.")
                validPhone = False
        
        address = input("Enter your address: ")
        customerList.append(address)
        
        #insert the new customer into the database
        try:
            dbconnection = sqlite3.connect('Assignment5.db')
            cursor = dbconnection.cursor()
            cursor.execute("""
                INSERT INTO customers (name, date_of_birth, contact_info, address)
                VALUES (?, ?, ?, ?)""", (tuple(customerList)))
            customerID = cursor.lastrowid #surrogate key ID value for the new customer data
            dbconnection.commit()
            dbconnection.close()
            print(f"New customer, {name}, added to database successfully!")
            return customerID
        except sqlite3.DatabaseError as dbError:
            print(f"Failed to add new customer, {name}, to database. Error: {dbError}.")
            sys.exit() #exit program if cannot execute/commit to database file

def GetDoctor(doctorName):
    try:
        dbconnection = sqlite3.connect('Assignment5.db')
        cursor = dbconnection.cursor()
        cursor.execute("Select id, name, contact_info, specialization from doctors")
        doctorList = cursor.fetchall()
        dbconnection.close()

        doctorID = 0
        for doctor in doctorList:
            if(doctor[1].title() == doctorName):
                doctorID = doctor[0]
                return doctorID #return valid doctor ID and their name
        return doctorID #return 0 if doctor not found and their name
    except sqlite3.DatabaseError as dbError:
        print(f"Error: {dbError}. Exiting program.")
        sys.exit() #gracefully exit program

def InsertDoctor(doctorName):
    doctorID = GetDoctor(doctorName)
    validPhone = False
    if(doctorID != 0): #doctor was found in the database
        return doctorID #return to main function if doctorID is found
    doctorList = []
    doctorList.append(doctorName)
    while(validPhone != True):
        doctorPhone = input("Enter your doctor's phone number (###-###-####): ")
        if((len(doctorPhone) == 12) and (doctorPhone[3] == '-') and (doctorPhone[7] == '-') and (doctorPhone.replace('-', '').isdigit())):
            doctorList.append(doctorPhone)
            validPhone = True
        else:
            print("Invalid phone number. Please type ###-###-#### as the format: ")
            validPhone = False
    doctorSpecialty = input("Enter your doctor's specialization: ")
    doctorList.append(doctorSpecialty)
    try:
        dbconnection = sqlite3.connect('Assignment5.db')
        cursor = dbconnection.cursor()
        cursor.execute("""Insert into doctors (name, contact_info, specialization) Values (?, ?, ?)""", tuple(doctorList))
        doctorID = cursor.lastrowid
        dbconnection.commit()
        dbconnection.close()
        print(f"{doctorName} has been added to the database successfully!")
        return doctorID #doctorID is associated with this function
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}. Cannot add {doctorName}. Exiting Program.")
        sys.exit() #exit program if cannot execute/commit to database file

def GetDrugs():
    try:
        dbconnection = sqlite3.connect('Assignment5.db')
        cursor = dbconnection.cursor()
        cursor.execute("Select id, drug_name, category, dosage_form, strength, price from drugs")
        dbDrugList = cursor.fetchall()
        dbconnection.close()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}. Cannot fetch drugs. Exiting Program.")
        sys.exit()
    
    quitSearch = False
    drugList = []
    while(quitSearch != True):
        drugSearchDict = {}
        drugSearch = input("Enter the drug you would like to search: ").title().strip()
    
        if(len(drugSearch) == 0): #cannot enter an empty string
            print("You entered an empty drug value! Try again.")
            quitSearch = False
            continue #restart outer loop iteration
        drugFound = False
        for drug in dbDrugList:
            if any(drug['Drug'] == drugSearch for drug in drugList): #if the user enters the same drug more than once, break out of for loop search
                print(f"The drug, {drugSearch}, has already been added.")
                drugFound = True
                break
            elif(drug[1] == drugSearch):
                drugSearchDict['ID'] = drug[0]
                drugSearchDict['Drug'] = drug[1]
                drugList.append(drugSearchDict) #append the dictionary to this list
                print(f"{drugSearch} was found in inventory.")
                drugFound = True
                break
        if(drugFound == False):
            print(f"{drugSearch} was not found in the inventory.")
        
        validInput = False
        while(validInput != True):
            continueSearch = input("Would you like to search for another drug? Y/N: ").lower().strip()
            if(continueSearch == "y"):
                validInput = True
                quitSearch = False
            elif(continueSearch == "n"):
                if(continueSearch == "n" and len(drugList) >= 1): #bypass next elif if they enter the drug more than once but type "n" (drugList is not empty, but drugSearchDict is empty)
                    validInput = True
                    quitSearch = True
                    break
                elif(continueSearch == "n" and len(drugSearchDict) == 0):
                    print("You must enter at least one drug to drop off a prescription.")
                    validInput = False
                    quitSearch = False
                    continue
                else:
                    validInput = True
                    quitSearch = True
            else:
                print("Invalid input. Please enter Y/N.")
                validInput = False
                quitSearch = False
    return drugList #return the list of drugs to be accessible to the rest of the program

def InsertDrugs(name, doctorName):
    #this function will be where the other functions are returned to, not the main
    customerID = InsertCustomer(name)
    print(f"{name}'s customer ID: {customerID}")
    doctorID = InsertDoctor(doctorName)
    print(f"{doctorName}'s doctor ID: {doctorID}")
    drugList = [] #will hold the list of dictionaries for drug ID and drug name
    drugList = GetDrugs()
    lst_prescriptionID = [] #keep track of this outside of for loop

    for drugs in drugList:
        validQty = False #reset validQty flag to prompt again for quantity prescribed
        prescriptionList = [] #append new customerID & doctorID (doesn't change), drugID will change each loop, quantity prescribed also
        prescriptionList.append(customerID)
        prescriptionList.append(doctorID)
        while(validQty == False):
            qtyPrescribed = input(f"Enter the quantity prescribed for {drugs['Drug']}: ")
            if(qtyPrescribed.isnumeric() and len(qtyPrescribed) > 0):
                if(int(qtyPrescribed) > 0):
                    validQty = True
                    qtyPrescribed = int(qtyPrescribed)
                    prescriptionList.append(drugs['ID']) #append the ID of the drug name
                    prescriptionList.append(qtyPrescribed) #append the qty prescribed
                else:
                    print("Enter a quantity greater than 0.")
                    validQty = False
            else:
                print("Invalid quantity. Please enter a number quantity.")
                validQty = False
        try:
            dbconnection = sqlite3.connect('Assignment5.db')
            cursor = dbconnection.cursor()
            cursor.execute("""Insert into prescriptions (customer_id, doctor_id, drug_id, prescription_date,
                        quantity_prescribed) Values (?, ?, ?, date('now'), ?)""",tuple(prescriptionList))
            prescriptionID = cursor.lastrowid
            lst_prescriptionID.append(prescriptionID) #append prescriptionID to list of prescription IDs
            dbconnection.commit()
            dbconnection.close()
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}. Cannot commit prescription for {drugs['Drug']} to database. Returning to main menu.")
            return 
    print("All drugs and their prescriptions have been added to the database.")
    print()

    #print receipt to Console and CustomerReceipt.txt in write mode
    placeholders = ','.join(['?'] * len(lst_prescriptionID)) # Create a string with the right number of placeholders based on the list length
    query = (f"""SELECT c.name, d.name, drugs.drug_name, p.quantity_prescribed, drugs.price
                            FROM prescriptions p
                                INNER JOIN customers c ON p.customer_id = c.id
                                INNER JOIN doctors d ON p.doctor_id = d.id
                                INNER JOIN drugs ON p.drug_id = drugs.id
                            WHERE p.id IN ({placeholders})""")
    try:
        dbconnection = sqlite3.connect('Assignment5.db')
        cursor = dbconnection.cursor()
        cursor.execute(query, lst_prescriptionID)
        prescriptionData = cursor.fetchall()
        dbconnection.close()
        with open('CustomerReceipt.txt', 'w') as receipt:
            receipt_text = (f"Prescription Receipt: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            receipt_text += (f"\nCustomer Name: {prescriptionData[0][0]}\n") #2D list in order to access specific values in prescriptionData, not the entire list at element[0]
            receipt_text += (f"Prescribing Doctor: {prescriptionData[0][1]}\n")
            prescriptionCount = 0 #keep track of drugs printed 
            totalCost = 0
            for row in prescriptionData:
                drugName = row[2]
                quantity = row[3]
                drugPrice = row[4]
                cost = quantity * drugPrice
                totalCost += cost
                prescriptionCount += 1
                receipt_text += (f"{prescriptionCount}. {drugName} - {quantity}        Cost: ${cost:.2f}\n")
            receipt.write(receipt_text)
            receipt.write(f"\nTotal due: ${totalCost:.2f}\n")
            #receipt.write("\n")
            #receipt.write("\n")
            print(f"View 'CustomerReceipt.txt' for prescription invoice.")
            print()
    except sqlite3.DatabaseError as e:
        print(f"Error occured: {e}. Cannot print receipt. Returning to main menu.")
        return #return to main menu

    print(f"Prescription Receipt: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    customerName = prescriptionData[0][0]
    doctorName = prescriptionData[0][1]

    print(f"Customer Name: {customerName}")
    print(f"Prescribing Doctor: {doctorName}")
    prescriptionCount = 0
    totalCost = 0
    
    print()
    for row in prescriptionData:
        drugName = row[2]
        quantity = row[3]
        drugPrice = row[4]
        cost = quantity * drugPrice
        totalCost += cost
        prescriptionCount += 1
        print(f"{prescriptionCount}) {drugName} - {quantity}        Cost: ${cost:.2f}")
    print(f"\nTotal due today: ${totalCost:.2f}\n")
    print()

def MenuOption():
    print("""Welcome to the Local Pharmacy.
1. Drop of a prescription
2. Exit""")
    menuOption = int(input("Choose your menu option: "))
    return menuOption

def Main(): #control the flow of the program
    exitProgram = False
    while(exitProgram != True):
        menuOption = MenuOption()
        match menuOption:
            case 1:
                validName = False
                while(validName != True): #customer name
                    firstName = input("Enter your first name: ").strip()
                    lastName = input("Enter your last name: ").strip()
                    if(len(firstName) == 0 or len(lastName) == 0):
                        print("Cannot have an empty name. Please re-enter your name.")
                        validName = False
                    else:
                        name = (firstName + ' ' + lastName).title()
                        validName = True
                #doctor code    
                valid_dr_fn = False
                valid_dr_ln = False
                while(valid_dr_fn != True):
                    doctorFn = input("Enter your doctor's first name: ").strip()
                    if(doctorFn.startswith("Dr.") or doctorFn.startswith("dr.") or len(doctorFn) == 0): #just enter a first name
                        print("Invalid doctor name. Only type your doctor's first name.")
                        valid_dr_fn = False
                    else:
                        valid_dr_fn= True
                while(valid_dr_ln != True):
                        doctorLn = input("Enter your doctor's last name: ").strip()
                        if(len(doctorLn) == 0):
                            print("Invalid last name. Cannot have an empty last name field.")
                            valid_dr_ln = False
                        else:
                            valid_dr_ln = True
                            doctorName = ("Dr. " + doctorFn + ' ' + doctorLn).title()
                InsertDrugs(name, doctorName)
            case 2:
                print("Exiting pharmacy interface...Goodbye!")
                exitProgram = True
            case _: #default case
                print("Invalid menu option. Please choose 1 or 2.")
Main()
