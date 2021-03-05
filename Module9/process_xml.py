import sys
import os

sys.path.append('D:\\Python_DQE\\Module5')
import publishing_input as pi
import xml.etree.ElementTree as ET

input_xml_name = 'xml_input.xml'
dict_xml_format = {'News': ('city', 'text'),
                   'PrivateAd': ('text', 'expiration_date'),
                   'Horoscope': ('period', 'zodiac_sign', 'prediction')}


def get_xml_data(p_path):
    print(f'\nLog: looking for file in {p_path}')
    try:
        with open(rf"{p_path}\\" + f"{input_xml_name}", "r+"):
            print('Log: file was found successfully!\n')
    except IOError:
        print('ERROR: file was not found\n')
        exit(0)
    try:
        data = ET.parse(f'{p_path}\\{input_xml_name}')
        return data
    except SyntaxError:
        print('ERROR: failed to parse xml, invalid file format')
        exit(0)


def validate_object_type(p_xml_data):
    print('Log: validating object types...')
    for obj_type in p_xml_data.getroot():
        if obj_type.tag not in dict_xml_format.keys():
            print('EXCEPTION: failed to parse, invalid object type:', obj_type.tag)
            exit(1)


def validate_object_params(p_xml_data):
    print('Log: validating object parameters...\n')
    root = p_xml_data.getroot()
    for child in root:
        list_of_expected_params = dict_xml_format.get(child.tag)
        number_of_params = sum(1 for _ in child.iter("*"))
        if len(list_of_expected_params) != number_of_params - 1:
            print('EXCEPTION: failed to parse, invalid number of parameters given for:', child.tag)
            exit(1)
        for item in child.iter():
            if item.tag not in dict_xml_format.keys() and item.tag not in list_of_expected_params:
                print('EXCEPTION: failed to parse, invalid parameter names given for', child.tag, '-', item.tag)
                exit(1)


def process_xml(p_xml_data):
    validate_object_type(p_xml_data)
    validate_object_params(p_xml_data)
    root = p_xml_data.getroot()
    for child in root:
        list_args = []
        for item in child.iter():
            if item.tag in dict_xml_format.keys():
                list_args.append(item.tag)
            else:
                list_args.append(item.text)
        list_args = tuple(list_args)
        print(f'Log: (XML) start creating object with parameters {list_args}')
        new_obj = eval('pi.' + 'Create' + list_args[0]).get_input_json_xml(*list_args)
        new_obj.publish(new_obj.prepare_output())


def main():
    xml_path = pi.get_path()
    xml_data = get_xml_data(xml_path)
    string_from_xml = ET.tostring(xml_data.getroot(), encoding='unicode')
    string_from_xml = string_from_xml.replace("\n", "")
    xml_data = ET.ElementTree(ET.fromstring(string_from_xml))
    process_xml(xml_data)
    pi.delete_file(xml_path, input_xml_name)


if __name__ == "__main__":
    main()
