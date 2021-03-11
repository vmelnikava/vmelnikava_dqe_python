import sys
sys.path.append('D:\\Python_DQE\\Module5')
import publishing_input as pi

dict_xml_format = {'News': ('city', 'text'),
                   'PrivateAd': ('text', 'expiration_date'),
                   'Horoscope': ('period', 'zodiac_sign', 'prediction')}

class processXml:
    def __init__(self, p_input_data):
        self.xml_data = p_input_data

    def validate_object_type(self):
        print('Log: validating object types...')
        for obj_type in self.xml_data.getroot():
            if obj_type.tag not in dict_xml_format.keys():
                print('EXCEPTION: failed to parse, invalid object type:', obj_type.tag)
                exit(1)

    def validate_object_params(self):
        print('Log: validating object parameters...\n')
        root = self.xml_data.getroot()
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

    def parse_xml(self):
        self.validate_object_type()
        self.validate_object_params()
        root = self.xml_data.getroot()
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
            param_list_db = new_obj.prepare_output_db()
            pi.publish_to_db(list_args[0], f"{param_list_db}")
