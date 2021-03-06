# --FORMAT REQUIREMENTS--
# File Name = batch_input.txt
# A line in a text file contains information about data type and all required parameters for it to be published
# each value in a line should be in double quotes
# each line starts from, data type value in double quotes followed by ':'
# all required parameters should be listed in double quotes after ':'
# separator between values does not matter
# Example: "News": "text value" "city value"

import re
import sys
sys.path.append('D:\\Python_DQE\\Module5')
import classNews, classPrivateAd, classHoroscope


class processBatch:
    def __init__(self, p_input_data):
        self.batch_data = p_input_data

    @staticmethod
    def validate_object_type(param_list):
        print('Log: validating object type...')
        if param_list[0] not in ('News', 'PrivateAd', 'Horoscope'):
            print('EXCEPTION: failed to parse, invalid object type')
            exit(1)

    @staticmethod
    def validate_parameters(param_list):
        print('Log: validating object parameters...')
        if (
                (param_list[0] == 'News' and len(param_list) != 3) or
                (param_list[0] == 'PrivateAd' and len(param_list) != 3) or
                (param_list[0] == 'Horoscope' and len(param_list) != 4)):
            print('EXCEPTION: failed to parse, invalid number of parameters given')
            exit(1)

    @staticmethod
    def publish_batch_record(record, param_list):
        new_obj = eval('class' + record[0] + '.create' + record[0]).get_input_batch(*param_list)
        new_obj.publish(new_obj.prepare_output())
        param_list_db = new_obj.prepare_output_db()
        new_obj.publish_to_db(f"{param_list_db}")

    def parse_batch(self):
        for one_record in re.findall(r'\"(.+)\"\:(.*)', self.batch_data):
            list_params = re.findall(r'\"([^\"]+)\"', one_record[1])
            list_params.insert(0, one_record[0])
            list_params = tuple(list_params)
            print(f'\nLog: start processing row {list_params}')
            self.validate_object_type(list_params)
            self.validate_parameters(list_params)
            self.publish_batch_record(one_record, list_params)
