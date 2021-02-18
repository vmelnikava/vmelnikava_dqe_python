from datetime import datetime, timedelta
import calendar
import re

type_dict = {'1': ('News', 'text', 'city', 'publish_date'),
             '2': ('PrivateAd', 'text', 'exp_date', 'days_left'),
             '3': ('Horoscope', 'period', 'zodiac sign', 'prediction', 'from_date', 'to_date')}


class CreateObjectDynamic:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_object_type(self):
        self.datatype = input('\nYour input: ')
        return self.datatype

    def validate_object_type(self):
        try:
            if self.datatype in self.kwargs.keys() or self.datatype == '0':
                self.show_object_type()
                return True
            else:
                print("Selected data type does not exist. Please try again or press 0 to exit.")
                return False
        except ValueError:
            print("This is not a valid input. Please try again or press 0 to exit.")
            return False

    def show_object_type(self):
        if self.datatype == '0':
            good_bye()
        print(f"""Selected data type: {self.kwargs[self.datatype][0]}""")
        return self.datatype

    def show_start(self):
        print(
            f"\nLog: Start creating {self.kwargs[self.datatype][0]} with parameters: {self.kwargs[self.datatype][1:]}")
        lst = self.kwargs[self.datatype]
        return lst

    def __format_output(self):
        my_str_first = self.args[0]
        for item in range(0, 30 - len(f'{self.args[0]}')):
            my_str_first += '-'
        return my_str_first

    def publish(self, p_output):
        my_str1 = self.__format_output()
        my_str2 = f"------------------------------\n"
        with open("newsfeed.txt", 'a+') as f:
            f.write(f"""{my_str1}\n{p_output}\n{my_str2}\n\n""")
        print(f"\nLog: Successfully published ({self.args[0]})!\n")


class CreateNews(CreateObjectDynamic):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.args = args

    @classmethod
    def get_input(cls, *args):
        p1_value = input(f"\nEnter {args[1]} for {args[0]}:")
        while not _is_valid_text(p1_value):
            p1_value = input(f"\nEnter {args[1]} for {args[0]}:")
        p2_value = input(f"\nEnter {args[2]} for {args[0]}:")
        while not _is_valid_text(p2_value):
            p2_value = input(f"\nEnter {args[2]} for {args[0]}:")
        print('\nLog: Calculating Publish Date...')
        p3_value = cls.calc_publish_date()
        return cls(args[0], p1_value, p2_value, p3_value)

    @staticmethod
    def calc_publish_date():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H.%M")

    def prepare_output(self):
        news_output = (
            f"""{self.args[1]}\n{self.args[2]}, {self.args[3]}""")
        return news_output


class CreatePrivateAd(CreateObjectDynamic):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.args = args

    @classmethod
    def get_input(cls, *args):
        p1_value = input(f"\nEnter {args[1]} for {args[0]}:")
        while not _is_valid_text(p1_value):
            p1_value = input(f"\nEnter {args[1]} for {args[0]}:")
        p2_value = input(f"\nEnter {args[2]} for {args[0]}:")
        while not _is_valid_date(p2_value):
            p2_value = input(f"\nEnter expiration date:")
        p3_value = str(cls.calc_days_left(p2_value)) + ' days left'
        print('\nLog: Calculating Days Left...')
        p2_value = 'Actual until: ' + p2_value
        return cls(args[0], p1_value, p2_value, p3_value)

    @staticmethod
    def calc_days_left(p_exp_date):
        today = datetime.today()
        exp_date = datetime.strptime(p_exp_date, '%d/%m/%Y')
        return (exp_date - today).days

    def prepare_output(self):
        ad_output = (
            f"""{self.args[1]}\n{self.args[2]}, {self.args[3]}""")
        return ad_output


class CreateHoroscope(CreateObjectDynamic):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.args = args

    @classmethod
    def get_input(cls, *args):
        p1_value = input(f"\nEnter {args[1]} for {args[0]}:")
        while not cls._is_valid_period(p1_value):
            p1_value = input(f"Enter {args[1]} for {args[0]}:")
        p2_value = input(f"\nEnter {args[2]} for {args[0]}:")
        while not _is_valid_text(p2_value):
            p2_value = input(f"\nEnter {args[2]} for {args[0]}:")
        p3_value = input(f"\nEnter {args[3]} for {args[0]}:")
        while not _is_valid_text(p3_value):
            p3_value = input(f"\nEnter {args[3]} for {args[0]}:")
        p4_value = cls.calc_from_date()
        p5_value = cls.calc_to_date(p1_value, p4_value)
        p4_value = p4_value.strftime('%b %d')
        p5_value = p5_value.strftime('%b %d')
        return cls(args[0], p1_value.capitalize(), str(p2_value).capitalize(), str(p3_value).capitalize(),
                   p4_value, p5_value)

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
        arg3 = '\n'.join(line.strip() for line in re.findall(r'.{1,30}(?:\s+|$)', self.args[3]))
        horoscope_output = (
            f"""{self.args[2]} {self.args[1]} Horoscope\n{self.args[4]} - {self.args[5]}\n{arg3}""")
        return horoscope_output


def _is_valid_text(p_str):
    if not p_str:
        print("!!!ERROR: input can not be empty. Please try again.")
        return False
    return True


def _is_valid_date(p_date):
    try:
        datetime.strptime(p_date, '%d/%m/%Y')
        return True
    except ValueError:
        print("!!!ERROR: incorrect date format, should be dd/mm/YYYY. Please try again.")
        return False


def print_data_types(p_dict):
    print("Enter a number of data type you'd like to publish (press 0 to exit) :")
    for key, value in p_dict.items():
        print('\t', p_dict[key][0], f"""({key})""")


def good_bye():
    print('Good Bye..')
    exit(0)


def proceed():
    question = input('Would you like to continue? Enter Y/N\n')
    if question.upper() == 'Y':
        main()
    elif question.upper() == 'N':
        good_bye()
    else:
        print('Incorrect input. Please try again.')
        proceed()


def main():
    print_data_types(type_dict)
    new_obj_d = CreateObjectDynamic(**type_dict)
    new_obj_d.get_object_type()
    while not new_obj_d.validate_object_type():
        new_obj_d.get_object_type()
    lst_param = new_obj_d.show_start()
    new_obj = eval('Create' + new_obj_d.kwargs[new_obj_d.datatype][0]).get_input(*lst_param)
    new_obj.publish(new_obj.prepare_output())
    proceed()


main()
