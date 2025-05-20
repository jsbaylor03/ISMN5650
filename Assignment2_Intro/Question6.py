# printing a 2D number pattern

#line = "" #will print the entire line each time

for i in range(1, 6): #controls the inner loop/rows
    line = "" #each time outer loop begins, line is initiated to an empty string
    for j in range(1, i + 1): #will increment j by 1 each time i increases and controls the columns
        line = line + str(j) + " "
    print(line)

# Easier method Mr. Farr showed me

#line = ""
#for i in range(1, 6):
#    line += str(i) + " "
#    print(line)