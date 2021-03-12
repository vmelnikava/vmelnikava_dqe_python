import classDynamicObject as d
from datetime import datetime


class createPrivateAd(d.CreateObjectDynamic):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.args = args

    @classmethod
    def get_input(cls, *args):
        p1_value = input(f"Enter {args[1]} for {args[0]}:")
        while not d.CreateObjectDynamic._is_valid_text(p1_value):
            p1_value = input(f"Enter {args[1]} for {args[0]}:")
        p2_value = input(f"Enter {args[2]} for {args[0]}:")
        while not d.CreateObjectDynamic._is_valid_date(p2_value):
            p2_value = input(f"Enter expiration date:")
        p3_value = str(cls.calc_days_left(p2_value)) + ' days left'
        print('Log: Calculating Days Left...')
        p2_value = 'Actual until: ' + p2_value
        return cls(args[0], p1_value, p2_value, p3_value)

    @classmethod
    def get_input_batch(cls, *args):
        p1_value = args[1]
        p2_value = args[2]
        p3_value = str(cls.calc_days_left(p2_value)) + ' days left'
        p2_value = 'Actual until: ' + p2_value
        # print('\nLog: Calculating Days Left...')
        return cls(args[0], p1_value, p2_value, p3_value)

    @classmethod
    def get_input_json_xml(cls, *args):
        if d.CreateObjectDynamic._is_valid_text(args[1]) and d.CreateObjectDynamic._is_valid_date(args[2]):
            return cls.get_input_batch(*args)
        else:
            print('\nLog: one of parameters failed validation, publishing was stopped')
            exit(1)

    @staticmethod
    def calc_days_left(p_exp_date):
        today = datetime.today()
        exp_date = datetime.strptime(p_exp_date, '%d/%m/%Y')
        return (exp_date - today).days

    def prepare_output(self):
        ad_output = (
            f"""{self.args[1]}\n{self.args[2]}, {self.args[3]}""")
        return ad_output

    def prepare_output_db(self):
        return self.args[1], self.args[2].split("Actual until: ", 1)[1]
