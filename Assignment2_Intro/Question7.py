userInput = input("Enter a positive integer: ")
userInput = int(userInput)

#need a sum variable to track total
sum = 0

#for loop to 
for i in range (1, userInput + 1): 
    sum += i #sum = sum + i (0+1+2+3+4...)
print("The sum of numbers 1 to " + str(userInput) + " is " + str(sum) + ".")