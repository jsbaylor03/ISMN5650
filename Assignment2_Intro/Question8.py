intNum = 550 # number hard-coded between 1 and 1000
boolInput = False
attempts = 0 #holds the number of attempts the user takes
#assume the user follows the prompt (no input check to see if # is between 1 and 1000)

while(boolInput == False):
    userInput = input("Enter a number between 1 and 1000: ")
    userInput = int(userInput)
    if (userInput > intNum):
        print("Your number is too big! Please try again.")
        print()
        attempts += 1
    elif(userInput < intNum):
        print("Your number is too small! Please try again.")
        print()
        attempts += 1
    else:
        print("You guessed it!")
        attempts += 1
        boolInput = True
print("Number of attempts: " + str(attempts)) 