import sys
sys.path.append('D:\\Python_DQE\\Module5')
import classNews, classPrivateAd, classHoroscope

dict_json_format = {'News': ('city', 'text'),
                    'PrivateAd': ('text', 'expiration date'),
                    'Horoscope': ('period', 'zodiac sign', 'prediction')}


class processJson:
    def __init__(self, p_input_data):
        self.json_data = p_input_data

    def validate_object_type(self):
        print('Log: validating object types...')
        for i in range(len(self.json_data)):
            if self.json_data[i].get('type') not in ('News', 'PrivateAd', 'Horoscope'):
                print('EXCEPTION: failed to parse, invalid object type:', self.json_data[i].get('type'))
                exit(1)

    def validate_object_params(self):
        print('Log: validating object parameters...')
        for i in range(len(self.json_data)):
            current_keys = self.json_data[i].keys()
            list_of_expected_params = dict_json_format.get(self.json_data[i].get('type'))
            if len(self.json_data[i].keys()) != len(list_of_expected_params) + 1:
                print('EXCEPTION: failed to parse, invalid number of parameters given for:\n', self.json_data[i])
                exit(1)
            for item in list_of_expected_params:
                if item not in current_keys:
                    print('EXCEPTION: failed to parse, invalid parameter names given for:\n', self.json_data[i])
                    exit(1)

    @staticmethod
    def publish_json_record(list_args):
        print(f'\nLog: (JSON) start processing row {list_args}')
        new_obj = eval('class' + list_args[0] + '.create' + list_args[0]).get_input_json_xml(*list_args)
        new_obj.publish(new_obj.prepare_output())
        param_list_db = new_obj.prepare_output_db()
        new_obj.publish_to_db(f"{param_list_db}")

    def parse_json(self):
        self.validate_object_type()
        self.validate_object_params()
        for item in self.json_data:
            list_args = tuple(item.values())
            self.publish_json_record(list_args)
