import csv
import re

file_words = 'count_words.csv'
file_letters = 'count_letters.csv'


def get_words():
    words = []
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')
        for row in reader:
            if row:
                csv_words = [i for i in re.findall(r'(\w+[\']*\w+)', row[0]) if not i.isdigit()]
                for i in csv_words:
                    words.append(i.lower())
    return words


def get_count_words(p_list_words):
    words_counted = []
    for word in p_list_words:
        x = p_list_words.count(word)
        words_counted.append((word, x))
    return [t for t in (set(tuple(i) for i in words_counted))]


def write_csv_words(p_list_word):
    with open(f'{file_path}\\' + file_words, 'w', newline='') as f:
        csv.register_dialect('our_dialect', delimiter='-', quoting=csv.QUOTE_NONE)
        writer = csv.writer(f, 'our_dialect')
        for item in p_list_word:
            writer.writerow([f'{item[0]}', f'{item[1]}'])


def get_letters():
    list_of_letters = []
    with open(input_file, 'r') as csvfile:
        csv_body = csvfile.read()
        csv_letters = [i for i in re.findall(r'[a-zA-Z]', csv_body)]
        for i in csv_letters:
            list_of_letters.append(i)
    # print('List of letters: ', list_of_letters)
    return list_of_letters


def get_count_letters(p_list_letters):
    letters_counted = []
    total_num_letters = len(p_list_letters)
    # print('Total number of letters =', total_num_letters)
    for i in p_list_letters:
        x = p_list_letters.count(i.lower())
        y = p_list_letters.count(i.upper())
        z = round(((x + y)/total_num_letters)*100, 2)
        letters_counted.append((i.lower(), x + y, y, z))
    # print('Letters counted: ', letters_counted)
    return [t for t in (set(tuple(i) for i in letters_counted))]


def write_csv_letters(p_list_letters):
    with open(f'{file_path}\\' + file_letters, 'w', newline='') as csvfile:
        headers = ['letter', 'count_all', 'count_uppercase', 'percentage']
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=',')
        writer.writeheader()
        for a, b, c, d in p_list_letters:
            writer.writerow({'letter': a, 'count_all': b, 'count_uppercase': c, 'percentage': d})


def main(p_path, p_file_name):
    global input_file, file_path
    file_path = p_path
    input_file = (f'{p_path}\\' + p_file_name)
    list_of_words = get_words()
    word_count = get_count_words(list_of_words)
    write_csv_words(word_count)
    list_of_letters = get_letters()
    letter_count = get_count_letters(list_of_letters)
    write_csv_letters(letter_count)


# validation of percentage sum
# with open(f'{file_path}\\' + file_letters, 'r', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     total_percentage = 0
#     for row in reader:
#         total_percentage += float(row['percentage'])
# print(total_percentage)
