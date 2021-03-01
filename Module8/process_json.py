import sys
import os
sys.path.append('D:\\Python_DQE\\Module5')
import publishing_input as pi
import json

default_json_path = 'D:\\Python_DQE\\Module6\\files'
input_json_name = 'json_input.json'

dict_json_format = {'News': ('city', 'text'),
                    'PrivateAd': ('text', 'expiration date'),
                    'Horoscope': ('period', 'zodiac sign', 'prediction')}


def get_path():
    input_path = input('Enter a path to file or leave it empty for default path:\n')
    if not input_path:
        input_path = default_json_path
    return input_path


def get_json_data(p_path):
    try:
        print(f'\nLog: looking for file in {p_path}')
        with open(rf"{p_path}\\" + f"{input_json_name}", "r+"):
            print('Log: file was found successfully!\n')
            return json.load(open(rf"{p_path}\\" + f"{input_json_name}"))
    except IOError:
        print('ERROR: file was not found\n')
        exit(0)


def validate_object_type(p_json_data):
    print('Log: validating object types...')
    for i in range(len(p_json_data)):
        if p_json_data[i].get('type') not in ('News', 'PrivateAd', 'Horoscope'):
            print('EXCEPTION: failed to parse, invalid object type:', p_json_data[i].get('type'))
            exit(1)


def validate_object_params(p_json_data):
    print('Log: validating object parameters...\n')
    for i in range(len(p_json_data)):
        current_keys = p_json_data[i].keys()
        list_of_expected_params = dict_json_format.get(p_json_data[i].get('type'))
        if len(p_json_data[i].keys()) != len(list_of_expected_params)+1:
            print('EXCEPTION: failed to parse, invalid number of parameters given for:\n', p_json_data[i])
            exit(1)
        for item in list_of_expected_params:
            if item not in current_keys:
                print('EXCEPTION: failed to parse, invalid parameter names given for:\n', p_json_data[i])
                exit(1)


def process_json(p_json_data):
    validate_object_type(p_json_data)
    validate_object_params(p_json_data)
    for item in p_json_data:
        list_args = tuple(item.values())
        print(f'Log: start creating object with parameters {list_args}')
        new_obj = eval('pi.' + 'Create' + list_args[0]).get_input_json(*list_args)
        new_obj.publish(new_obj.prepare_output())


def delete_file(p_path, p_file_name):
    print('Log: start deleting input file..')
    try:
        os.remove(rf"{p_path}\\" + f"{p_file_name}")
    except IOError:
        print('EXCEPTION: failed to delete the file')
    print('Log: input file has been deleted')


def main():
    json_path = get_path()
    json_data = get_json_data(json_path)
    process_json(json_data)
    delete_file(json_path, input_json_name)


if __name__ == "__main__":
    main()
