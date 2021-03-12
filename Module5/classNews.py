import classDynamicObject as d
from datetime import datetime


class createNews(d.CreateObjectDynamic):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.args = args

    @classmethod
    def get_input(cls, *args):
        p1_value = input(f"Enter {args[1]} for {args[0]}:")
        while not d.CreateObjectDynamic._is_valid_text(p1_value):
            p1_value = input(f"Enter {args[1]} for {args[0]}:")
        p2_value = input(f"Enter {args[2]} for {args[0]}:")
        while not d.CreateObjectDynamic._is_valid_text(p2_value):
            p2_value = input(f"Enter {args[2]} for {args[0]}:")
        print('Log: calculating publish date...')
        p3_value = cls.calc_publish_date()
        return cls(args[0], p1_value, p2_value, p3_value)

    @classmethod
    def get_input_batch(cls, *args):
        p1_value = args[1]
        p2_value = args[2]
        p3_value = cls.calc_publish_date()
        return cls(args[0], p1_value, p2_value, p3_value)

    @classmethod
    def get_input_json_xml(cls, *args):
        if d.CreateObjectDynamic._is_valid_text(args[1]) and d.CreateObjectDynamic._is_valid_text(args[2]):
            return cls.get_input_batch(*args)
        else:
            print('\nLog: one of parameters is empty, publishing was stopped')
            exit(1)

    @staticmethod
    def calc_publish_date():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H.%M")

    def prepare_output(self):
        news_output = (
            f"""{self.args[1]}\n{self.args[2]}, {self.args[3]}""")
        return news_output

    def prepare_output_db(self):
        return self.args[1], self.args[2]
