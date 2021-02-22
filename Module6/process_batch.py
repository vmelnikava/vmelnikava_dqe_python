# --FORMAT REQUIREMENTS--
# File Name = batch_input.txt
# A line in a text file contains information about data type and all required parameters for it to be published
# each value in a line should be in double quotes
# each line starts from, data type value in double quotes followed by ':'
# all required parameters should be listed in double quotes after ':'
# separator between values does not matter
# Example: "News": "text value" "city value"

import sys
sys.path.append('D:\\Python_DQE\\Module5')
import re
import os
import publishing_input as pi


default_input_path = 'D:\\Python_DQE\\Module6\\files'
input_file_name = 'batch_input.txt'


def search_file(p_path):
    try:
        print(f'\nLog: looking for file in {p_path}')
        with open(rf"{p_path}\\" + f"{input_file_name}", "r+") as f:
            print('Log: file was found successfully!\n')
            return f.read()
    except IOError:
        print('ERROR: file was not found\n')
        exit(0)


def get_path():
    return input('Enter a path to file or leave it empty for default path:\n')


def parse_batch(p_input_data):
    for one_record in re.findall(r'\"(.+)\"\:(.*)', p_input_data):
        list_params = re.findall(r'\"([^\"]+)\"', one_record[1])
        list_params.insert(0, one_record[0])
        list_params = tuple(list_params)
        print(f'Log: start processing row {list_params}')
        if list_params[0] not in ('News', 'PrivateAd', 'Horoscope'):
            print('EXCEPTION: failed to parse, invalid object type')
            exit(1)
        if (
                (list_params[0] == 'News' and len(list_params) != 3) or
                (list_params[0] == 'PrivateAd' and len(list_params) != 3) or
                (list_params[0] == 'Horoscope' and len(list_params) != 4)):
            print('EXCEPTION: failed to parse, invalid number of parameters given')
            exit(1)
        new_obj = eval('pi.' + 'Create' + one_record[0]).get_input_batch(*list_params)
        new_obj.publish(new_obj.prepare_output())


def delete_file(p_path):
    print('Log: start deleting input file..')
    try:
        os.remove(rf"{p_path}\\" + f"{input_file_name}")
    except IOError:
        print('EXCEPTION: failed to delete the file')
    print('Log: input file has been deleted')


def main():
    input_path = get_path()
    if not input_path:
        input_path = default_input_path
    data = search_file(input_path)
    parse_batch(data)
    delete_file(input_path)


if __name__ == "__main__":
    main()
