import re
import random as r
import string as s

# ---------------- HOME TASK 3 FUNCTIONS ----------------


def find_sentence(p_input_str):
    return re.findall(r'[^.?!:]+[.?!:]+', p_input_str)


def find_first_word(p_sentence):
    return re.search(r'(\w+)', p_sentence).group()


def capitalize_sentence(p_sentence, p_word):
    return p_sentence.replace(p_word, p_word.capitalize())


def normalize(input_str):
    nmlz_str = ''
    input_str = input_str.capitalize()
    for item in find_sentence(input_str):
        nmlz_str += capitalize_sentence(item, find_first_word(item))
    return nmlz_str


def last_words(input_str, mysubstr):
    lw_str = (' '.join(re.findall(r'\s*(\w+)\s*[.:!?]', input_str)).capitalize()) + '.'
    return (mysubstr + ' ' + lw_str).join(input_str.split(mysubstr))


def replace_word(input_str, old_value, new_value):
    return re.sub(rf"(?i)(?<=\s){old_value}(?=\s)", new_value, input_str)


def count_whitespaces(input_str):
    return sum(1 for i in input_str if i.isspace() is True)


# ---------------- HOME TASK 2 FUNCTIONS ----------------


rand_num = lambda x, y: r.randint(x, y)


def create_dict():
    return {r.choice(s.ascii_lowercase): rand_num(0, 100) for x in range(rand_num(1, 28))}


def generate_list_dict(func):
    my_list = []
    for j in range(0, func):
        my_list.append(create_dict())
    return my_list


get_dict_with_max_key = lambda temp_dict: max(temp_dict, key=temp_dict.get)


def insert_into_dict(p_dict, p_key, p_value, p_suffix):
    if p_suffix is None:
        p_dict[p_key] = p_value
    else:
        p_dict[p_key + '_' + str(p_suffix + 1)] = p_value


def check_key_exists(p_dict, p_key):
    exist_flag = False
    for key_f in p_dict.keys():
        if [p_key] in (key_f.split('_')[:-1], key_f):
            exist_flag = True
            if exist_flag:
                break
    return exist_flag


def get_values_for_key(p_list, p_key, p_pos):
    pos = p_pos
    temp_dict = {}
    while pos < len(p_list):
        if p_list[pos].get(p_key, 'N/A') != 'N/A':
            temp_dict[pos] = p_list[pos].get(p_key, 'N/A')
        pos += 1
    return temp_dict


def create_common_dict(p_list):
    dict_final = {}
    for i in range(len(p_list)):
        for key, value in p_list[i].items():
            if not check_key_exists(dict_final, key):
                d = get_values_for_key(p_list, key, i)
                if len(d) == 1:
                    insert_into_dict(dict_final, key, value, None)
                else:
                    dict_with_max_key = get_dict_with_max_key(d)
                    insert_into_dict(dict_final, key, d[dict_with_max_key], dict_with_max_key)
    return dict_final

# ---------------- HOME TASK 3 MAIN CODE ----------------


str1 = "my name IS VOLHA, last name is Melnikava   .    and i live in MINSK, thank you!! how are YOU? where are yoU????"
print('Input string:\n', str1)

str2 = normalize(str1)
print('Normalized string:\n', str2)

str3 = last_words(str2, '!!')
print('String updated with last words:\n', str3)

str4 = replace_word(str3, 'volha', 'Denis')
print('String with replaced word:\n', str4)

print('Number of whitespaces:\n', count_whitespaces(str1))

# ---------------- HOME TASK 2 MAIN CODE ----------------
generated_list = generate_list_dict(rand_num(2, 10))
print('Generated list of dictionaries:\n', generated_list)

common_dict = create_common_dict(generated_list)
print('Common Dictionary:', common_dict)
