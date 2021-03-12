import classDynamicObject as d
from datetime import datetime, timedelta
import calendar


class createHoroscope(d.CreateObjectDynamic):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.args = args

    @classmethod
    def get_input(cls, *args):
        p1_value = input(f"Enter {args[1]} for {args[0]}:")
        while not cls._is_valid_period(p1_value):
            p1_value = input(f"Enter {args[1]} for {args[0]}:")
        p2_value = input(f"Enter {args[2]} for {args[0]}:")
        while not d.CreateObjectDynamic._is_valid_text(p2_value):
            p2_value = input(f"Enter {args[2]} for {args[0]}:")
        p3_value = input(f"Enter {args[3]} for {args[0]}:")
        while not d.CreateObjectDynamic._is_valid_text(p3_value):
            p3_value = input(f"Enter {args[3]} for {args[0]}:")
        p4_value = cls.calc_from_date()
        p5_value = cls.calc_to_date(p1_value, p4_value)
        p4_value = p4_value.strftime('%b %d')
        p5_value = p5_value.strftime('%b %d')
        return cls(args[0], p1_value.capitalize(), str(p2_value).capitalize(), str(p3_value).capitalize(),
                   p4_value, p5_value)

    @classmethod
    def get_input_batch(cls, *args):
        p1_value = args[1]
        p2_value = args[2]
        p3_value = args[3]
        p4_value = cls.calc_from_date()
        p5_value = cls.calc_to_date(p1_value, p4_value)
        p4_value = p4_value.strftime('%b %d')
        p5_value = p5_value.strftime('%b %d')
        return cls(args[0], p1_value.capitalize(), str(p2_value).capitalize(), str(p3_value).capitalize(),
                   p4_value, p5_value)

    @classmethod
    def get_input_json_xml(cls, *args):
        if cls._is_valid_period(args[1]) and d.CreateObjectDynamic._is_valid_text(args[2]) and \
                d.CreateObjectDynamic._is_valid_text(args[3]):
            return cls.get_input_batch(*args)
        else:
            print('\nLog: one of parameters failed validation, publishing was stopped')
            exit(1)

    @staticmethod
    def _is_valid_period(p_period):
        if not (p_period in ('daily', 'weekly', 'monthly')):
            print("!!!ERROR: incorrect time period. Possible values are: daily/weekly/monthly. Please try again.")
            return False
        return True

    @staticmethod
    def calc_from_date():
        tomorrow = datetime.today().date() + timedelta(days=1)
        return tomorrow

    @staticmethod
    def calc_to_date(period, from_date):
        delta_dict = {
            'daily': from_date + timedelta(days=1),
            'weekly': from_date + timedelta(weeks=1),
            'monthly': from_date + timedelta(days=calendar.monthrange(from_date.year, from_date.month)[1])}
        return delta_dict[period]

    def prepare_output(self):
        # arg3 = '\n'.join(line.strip() for line in re.findall(r'.{1,30}(?:\s+|$)', self.args[3]))
        horoscope_output = (
            f"""{self.args[2]} {self.args[1]} Horoscope\n{self.args[4]} - {self.args[5]}\n{self.args[3]}""")
        return horoscope_output

    def prepare_output_db(self):
        return self.args[1], self.args[2], self.args[3]
