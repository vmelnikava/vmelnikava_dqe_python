# import random module in order to generate random number
import random as r
# import string module in order to generate random letter
import string as s
# create new empty list to store all dictionaries
my_list = []
# create new variable to count dictionaries
i = 0
# generate random number to be used for number of dictionaries or length of list
list_len = r.randint(2, 10)
# print how many dictionaries need to be generated
print(list_len, 'dictionaries need to be generated')

# use while to populate list with required number of dictionaries
while i < list_len:
    # use comprehension to create new dictionary and append it to a list
    # dict key is a random letter, dict value is a random int, each dict has random length
    my_list.append({r.choice(s.ascii_lowercase): r.randint(0, 100) for n in range(r.randint(1, 28))})
    # move to the next iteration to create another dictionary
    i += 1

# print list of dictionaries
print('Generated list of dictionaries:', my_list)

# i = number of dictionary in the list
i = 0
# create new empty dictionary for final results
dict_final = {}

# starting a loop to go through each dictionary in a list
for i in range(len(my_list)):
    # loop to work with each pair of key-value in current dictionary
    for key, value in my_list[i].items():
        # introducing boolean variable to mark whether key exists in final dictionary or not
        flag = False
        # going through each key in final dictionary to verify whether current key exists there or not
        for key_f in dict_final.keys():
            # comparing curr key with either split key ('a_1') from final dict or wih just a key ('a')
            if [key] in (key_f.split('_')[:-1], key_f):
                # setting flag to True to indicate that current key already exists in final dictionary
                flag = True
            # if key was found in final dictionary
            if flag:
                # exist loop 'for', no need to compare curr key with other keys from final dict
                break
        # actions if current key was not found in final dictionary
        if not flag:
            # introduce a counter for dictionaries in a list
            n = i
            # create new dict to store temp results
            d = {}
            # use while loop to find current key in all dictionaries
            while n < len(my_list):
                # checking if current key exists in each dictionary
                if my_list[n].get(key, 'N/A') != 'N/A':
                    # if it does, move its value and number of its dictionary to temp dictionary
                    d[n] = my_list[n].get(key, 'N/A')
                # increase counter to move to check whether key exists in next dictionary
                n += 1
            # checking length of temp dictionary to know how many times this key appears
            if len(d) == 1:
                # key appears only in 1 dictionary, hence inserting new key-value pair in final dict (without dict #)
                dict_final[key] = value
            else:
                # key appears in more than 1 dict, hence need to calculate max value from temp dictionary
                dict_with_max_key = max(d, key=d.get)
                # insert new key-value pair into the final dict with max value and appropriate key (with dict #)
                dict_final[key + '_' + str(dict_with_max_key+1)] = d[dict_with_max_key]
# print final dictionary
print('Common Dictionary:', dict_final)
