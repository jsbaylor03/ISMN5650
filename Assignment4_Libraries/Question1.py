import csv
import sys

inventory_file = "Inventory.csv"
summary_file = "Summary.txt"
detail_file = "Detail.txt"
errors_file = "Errors.csv"

def ReadCSVFile(inventory_file):
    inv_read_success = False
    try:
        with open(inventory_file, "r") as inventoryCSV:
            csv_reader = csv.reader(inventoryCSV) #read csv file into csv_reader variable as a list
            data = []
            for row in csv_reader:
                data.append(row) #collect each row/record as a list element
        print(f"Stored {inventory_file} contents into memory.")
        inv_read_success = True
        return data, inv_read_success
    except FileNotFoundError: #just in case the file is deleted/does not exist. The file is critical to the program so terminate if not found.
        print(f"{inventory_file} does not exist.")
        return None, inv_read_success #remains null value (none) and false
    
def AppendErrors(access_csv):
    #this is just for the console to see for validation
    valid_id_count = 0
    valid_amt_count = 0
    valid_qty_count = 0
    valid_item_count = 0
    valid_state_count = 0
    #these variables store the errors into a separate list to be used for errors function later in program
    missingID = []
    invalidAmount = []
    invalidQty = []
    missingItem = []
    missingState = []
    for rowID in access_csv[1:]: #skip the header row although I could have done it when reading in the file initially
        if (rowID[0].isdigit()):  #checks to see if data type is numeric/non-empty
            valid_id_count += 1
        else:
            missingID.append(rowID) #append the entire row with missingID 
    for rowAmt in access_csv[1:]:
        if (rowAmt[1].isdigit()):
            valid_amt_count += 1
        else:
            invalidAmount.append(rowAmt)
    for rowItem in access_csv[1:]:
        if (rowItem[2] != ""):
            valid_item_count += 1
        else:
            missingItem.append(rowItem)
    for rowQty in access_csv[1:]:
        if (rowQty[3].isdigit()): #requires knowledge/structure of input csv
            valid_qty_count += 1
        else:
            invalidQty.append(rowQty)
    for rowState in access_csv[1:]:
        if(rowState[4] != ""):
            valid_state_count += 1
        else:
            missingState.append(rowState)

    print(f"Number of rows with valid IDs: {valid_id_count}")
    print(f"Number of rows with valid amount field: {valid_amt_count}")
    print(f"Number of rows with valid item field: {valid_item_count}")
    print(f"Number of rows with valid quantity field: {valid_qty_count}")
    print(f"Number of rows with valid state field: {valid_state_count}")

    #return these values for later access
    return missingID, invalidAmount, missingItem, invalidQty, missingState

def WriteDetailTxt(access_csv):
    validRows = []

    for row in access_csv[1:]: #check to see if row elements/columns are empty strings (if so, they are excluded from validRows)
        if (
            row[0] != "" and 
            row[1] != "" and 
            row[2] != "" and 
            row[3] != "" 
        ):
            validRows.append(row)  # Append valid rows

    with open(detail_file, 'w', encoding='UTF8') as detailTXT: #if file does not exist, detail_file will be created 
        for row in validRows:
            detailTXT.write(f"{row[0]:<10}{row[1].zfill(10)}{row[2]:<40}{row[3]:<10}{row[4]:<20}\n")  #zfill() pads with zeros
    return validRows #will be used to write the summary file

def WriteErrorsCSV(missingID, invalidAmount, missingItem, invalidQty, missingState, errors_file):
    with open(errors_file, 'w', newline='', encoding='UTF8') as errorsCSV: #newline is single return
        writer = csv.writer(errorsCSV)

        if len(missingID) > 0: #if missingID list has contents within it, set errorCode = 1
            errorCode = 1
            for record in missingID:
                writer.writerow(record + [str(errorCode)]) #errorCode has to be concatenated as an additional element to the record in order for writerow() to function
        if len(invalidAmount) > 0:
            errorCode = 2
            for record in invalidAmount:
                writer.writerow(record + [str(errorCode)])
        if len(missingItem) > 0:
            errorCode = 3
            for record in missingItem:
                writer.writerow(record + [str(errorCode)])
        if len(invalidQty) > 0:
            errorCode = 4
            for record in invalidQty:
                writer.writerow(record + [str(errorCode)])
        if len(missingState) > 0:
            errorCode = 5
            for record in missingState:
                writer.writerow(record + [str(errorCode)]) 

def WriteSummaryTxt(validRows, summary_file):
    row_count = 0
    sum_amount = 0
    sum_qty = 0
    for rowID in validRows:
        if(rowID[0].isdigit()): #will always be a digit since we are looking in the validRows list (merely for code to function/rowID to be accessed)
            row_count += 1
    for rowAmt in validRows:
        sum_amount += int(rowAmt[1])
    for rowQty in validRows:
        sum_qty += int(rowQty[3])
    with open(summary_file, 'w') as summaryTXT:
        summaryTXT.write(f"{row_count:<10}{sum_amount:<10}{sum_qty:<10}")  #will match the data from detail.txt file as validation

#calling functions at the bottom of code

def main():

    access_csv, inv_read_success = ReadCSVFile(inventory_file) # Read the CSV data into a list (data = access_csv)

    if not inv_read_success: #if inv_read_success not true
        print(f"Terminating program due to missing {inventory_file} file.")
        sys.exit() #exits program completely if inventory_file is not found/deleted for some reason

    missingID, invalidAmount, missingItem, invalidQty, missingState = AppendErrors(access_csv) #collects rows in access_csv with errors
    WriteErrorsCSV(missingID, invalidAmount, missingItem, invalidQty, missingState, errors_file) #writes the multiple lists of errors in errors.csv file
    validRows = WriteDetailTxt(access_csv) #write to the detail.txt file, stored in validRows to be used by WriteSummaryTxt
    WriteSummaryTxt(validRows, summary_file) #write the validation of detail.txt file
    print(f"The output files {summary_file}, {detail_file}, and {errors_file} can now be reviewed for internal use.")

main()
    