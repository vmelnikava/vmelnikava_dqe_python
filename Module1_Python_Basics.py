# import random module to use its functions
import random as r
# create an empty list to be populated with random numbers
list_num = []
# create an empty list for sorting
sorted_list = []
# introduce and set value for length of list
n = 100
# create a variable to count even numbers
count_even = 0
# create a variable to count odd numbers
count_odd = 0
# create a variable for sum of even numbers
sum_even = 0
# create a variable for sum of odd numbers
sum_odd = 0
# create a variable for average of even numbers
avg_even = 0
# create a variable for average of odd numbers
avg_odd = 0

# use 'for' to get 100 random numbers, a sequence of integers will be returned in range 0-99
for i in range(n):
    # add to the list a random number from specified range using randint function
    list_num.append(r.randint(0, 1000))

# print generated list of 100 numbers
print("List of 100 random numbers:\n", list_num)

# repeat until list is not empty
while list_num:
    # set minimum value to first element from the list
    min_value = list_num[0]
    # repeat for each element in the list
    for x in list_num:
        # identify minimum value from all elements in the list through a simple comparison
        if x < min_value:
            # if element from the list is less than current minimum then set it as a minimum value
            min_value = x
    # Add minimum value as a new element to sorted list
    sorted_list.append(min_value)
    # Remove minimum value from initial list of random values
    list_num.remove(min_value)

# print sorted list of 100 numbers
print('Sorted list of 100 random numbers:\n', sorted_list)

# repeat for each element from sorted list
for i in range(n):
    # calculate remainder after division using modulus. If modulus does not return zero
    if sorted_list[i] % 2 != 0:
        # it is an odd number, add its value sum of all odd numbers
        sum_odd += sorted_list[i]
        # increase count of odd numbers by one
        count_odd += 1
    # If modulus returns a zero
    else:
        # it is an even number, add its value to sum of all even numbers
        sum_even += sorted_list[i]
        # increase count of even numbers by one
        count_even += 1

# print sum of odd numbers from sorted list
print("sum_odd =", sum_odd)
# print count of odd numbers from sorted list
print("count_odd =", count_odd)
# print sum of even numbers from sorted list
print("sum_even =", sum_even)
# print count of even numbers from sorted list
print("count_even =", count_even)
# calculate average value for even numbers
avg_even = sum_even / count_even
# calculate average value for odd numbers
avg_odd = sum_odd / count_odd
# print average value for even numbers
print("Average for even numbers =", avg_even)
# print average value for odd numbers
print("Average for odd numbers =", avg_odd)
