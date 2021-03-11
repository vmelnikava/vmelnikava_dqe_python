import sys
sys.path.append('D:\\Python_DQE\\Module5')
sys.path.append('D:\\Python_DQE\\Module4')
sys.path.append('D:\\Python_DQE\\Module7')
sys.path.append('D:\\Python_DQE\\Module8')
sys.path.append('D:\\Python_DQE\\Module9')
import os
import json
import xml.etree.ElementTree as ET
import publishing_input as pi
import functions as f
import generate_csv
import classBatch
import classJson
import classXml

batch_file_name = 'batch_input.txt'
default_file_path = 'D:\\Python_DQE\\Module6\\files'
json_file_name = 'json_input.json'
xml_file_name = 'xml_input.xml'


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
    with open(rf"{pi.default_output_path}\\" + "newsfeed_input.txt", 'r') as file:
        norm_data = f.normalize(file.read())
    norm_data = norm_data.replace('Privatead', 'PrivateAd')
    with open(rf"{pi.default_output_path}\\" + "newsfeed_input.txt", 'w') as file:
        file.write(norm_data)
    print('Log: case normalization was successfully applied!\n')


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
    print('Log: start deleting input file..')
    try:
        os.remove(rf"{p_path}\\" + f"{p_file_name}")
    except IOError:
        print('EXCEPTION: failed to delete the file')
    print('Log: input file has been deleted')


def main():
    mode = select_mode()
    if mode == '1':
        pi.main()
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
        pi.good_bye()
    else:
        print('ERROR: incorrect input (1,2,3 or 4 is expected)')
        exit(0)
    normalize_file()
    generate_csv.main(pi.default_output_path, pi.output_file_name)
    pi.good_bye()


main()
