import sys
sys.path.append('D:\\Python_DQE\\Module5')
sys.path.append('D:\\Python_DQE\\Module4')
sys.path.append('D:\\Python_DQE\\Module7')
sys.path.append('D:\\Python_DQE\\Module8')
sys.path.append('D:\\Python_DQE\\Module9')
import os
import json
import xml.etree.ElementTree as ET
import functions as f
import generate_csv
import classBatch
import classJson
import classXml
import classDynamicObject as d
import classNews, classHoroscope, classPrivateAd

default_file_path = 'D:\\Python_DQE\\Module6\\files'
batch_file_name = 'batch_input.txt'
json_file_name = 'json_input.json'
xml_file_name = 'xml_input.xml'

type_dict = {'1': ('News', 'text', 'city', 'publish_date'),
             '2': ('PrivateAd', 'text', 'exp_date', 'days_left'),
             '3': ('Horoscope', 'period', 'zodiac sign', 'prediction', 'from_date', 'to_date')}


def print_data_types():
    print("Enter a number of data type you'd like to publish (press 0 to exit) :")
    for key, value in type_dict.items():
        print('\t', type_dict[key][0], f"""({key})""")


def good_bye():
    print('Good Bye..')
    exit(0)


def proceed():
    question = input('\nWould you like to continue? Enter Y/N\n')
    if question.upper() == 'Y':
        main()
    elif question.upper() == 'N':
        pass
    else:
        print('Incorrect input. Please try again.')
        proceed()


def select_mode():
    mode = input(f"""Enter which mode you would like to run publishing:
    1 - Input Mode
    2 - Batch Mode
    3 - JSON Mode
    4 - XML Mode
    0 - Exit\nYour Input:\n""")
    return mode


def normalize_file():
    print('\nLog: applying case normalization to newsfeed')
    with open(rf"{d.default_output_path}\\" + "newsfeed_input.txt", 'r') as file:
        norm_data = f.normalize(file.read())
    norm_data = norm_data.replace('Privatead', 'PrivateAd')
    with open(rf"{d.default_output_path}\\" + "newsfeed_input.txt", 'w') as file:
        file.write(norm_data)
    print('Log: case normalization was successfully applied!')


def get_path():
    input_path = input('Enter a path to file or leave it empty for default path:\n')
    if not input_path:
        input_path = default_file_path
    return input_path


def search_file(p_path, p_file_name):
    try:
        print(f'\nLog: looking for file in {p_path}')
        with open(rf"{p_path}\\" + f"{p_file_name}", "r+") as f:
            print('Log: file was found successfully!\n')
            return f.read()
    except IOError:
        print('ERROR: file was not found\n')
        exit(0)


def search_json(p_path, p_file_name):
    print(f'\nLog: looking for file in {p_path}')
    try:
        with open(rf"{p_path}\\" + f"{p_file_name}", "r+"):
            print('Log: file was found successfully!\n')
            return json.load(open(rf"{p_path}\\" + f"{p_file_name}"))
    except IOError:
        print('ERROR: file was not found\n')
        exit(0)


def search_xml(p_path, p_file_name):
    print(f'\nLog: looking for file in {p_path}')
    try:
        with open(rf"{p_path}\\" + f"{p_file_name}", "r+"):
            print('Log: file was found successfully!\n')
    except IOError:
        print('ERROR: file was not found\n')
        exit(0)
    try:
        data = ET.parse(f'{p_path}\\{p_file_name}')
        return data
    except SyntaxError:
        print('ERROR: failed to parse xml, invalid file format')
        exit(0)


def delete_file(p_path, p_file_name):
    print('\nLog: start deleting input file..')
    try:
        os.remove(rf"{p_path}\\" + f"{p_file_name}")
    except IOError:
        print('EXCEPTION: failed to delete the file')
    print('Log: input file has been deleted')


def main():
    mode = select_mode()
    if mode == '1':
        print_data_types()
        new_obj_d = d.CreateObjectDynamic(**type_dict)
        new_obj_d.get_object_type()
        while not new_obj_d.validate_object_type():
            new_obj_d.get_object_type()
        lst_param = new_obj_d.show_start()
        new_obj = eval('class' + new_obj_d.kwargs[new_obj_d.datatype][0] + '.create' +
                       new_obj_d.kwargs[new_obj_d.datatype][0]).get_input(*lst_param)
        new_obj.publish(new_obj.prepare_output())
        param_list_db = new_obj.prepare_output_db()
        new_obj.publish_to_db(f"{param_list_db}")
    elif mode == '2':
        batch_path = get_path()
        file_data = search_file(batch_path, batch_file_name)
        batch = classBatch.processBatch(file_data)
        batch.parse_batch()
        delete_file(batch_path, batch_file_name)
    elif mode == '3':
        json_path = get_path()
        file_data = search_json(json_path, json_file_name)
        my_json = classJson.processJson(file_data)
        my_json.parse_json()
        delete_file(json_path, json_file_name)
    elif mode == '4':
        xml_path = get_path()
        file_data = search_xml(xml_path, xml_file_name)
        string_from_xml = ET.tostring(file_data.getroot(), encoding='unicode')
        string_from_xml = string_from_xml.replace("\n", "")
        file_data = ET.ElementTree(ET.fromstring(string_from_xml))
        my_xml = classXml.processXml(file_data)
        my_xml.parse_xml()
        delete_file(xml_path, xml_file_name)
    elif mode == '0':
        good_bye()
    else:
        print('ERROR: incorrect input (1,2,3 or 4 is expected)')
        good_bye()
    normalize_file()
    d.CreateObjectDynamic.query_db('News')
    d.CreateObjectDynamic.query_db('PrivateAd')
    d.CreateObjectDynamic.query_db('Horoscope')
    generate_csv.main(d.default_output_path, d.output_file_name)
    d.CreateObjectDynamic.find_duplicates()
    proceed()
    good_bye()


main()
