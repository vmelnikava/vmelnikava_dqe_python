import sys
sys.path.append('D:\\Python_DQE\\Module10')
import classDB
import classDuplicates
from datetime import datetime

default_output_path = 'D:\\Python_DQE\\Module6\\files'
output_file_name = 'newsfeed_input.txt'


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
            print('Good bye!')
            exit(0)
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
        with open(rf"{default_output_path}\\" + output_file_name, "a+") as f:
            f.write(f"""{my_str1}\n{p_output}\n{my_str2}\n\n""")
        print(f"Log: successfully published to file ({self.args[0]})")

    def publish_to_db(self, param_list):
        my_connection = classDB.DBConnection(rf'{classDB.sqlitedb_path}\publishing.db')
        my_connection.create_table('News', 'text text, city text')
        my_connection.create_table('PrivateAd', 'text text, exp_date date')
        my_connection.create_table('Horoscope', 'period text, zodiac_sign text, prediction text')
        print(f'Log: inserting new row into sqlite table ({self.args[0]})')
        my_connection.insert_row(self.args[0], param_list)
        my_connection.commit_changes()
        print(f'Log: successfully published to sqlite ({self.args[0]})')
        my_connection.cursor.close()

    @staticmethod
    def _is_valid_text(p_str):
        if not p_str:
            print("!!!ERROR: input can not be empty. Please try again.")
            return False
        return True

    @staticmethod
    def _is_valid_date(p_date):
        try:
            datetime.strptime(p_date, '%d/%m/%Y')
            return True
        except ValueError:
            print("!!!ERROR: incorrect date format, should be dd/mm/YYYY. Please try again.")
            return False

    @staticmethod
    def query_db(table_name):
        my_connection = classDB.DBConnection(rf'{classDB.sqlitedb_path}\publishing.db')
        print(f'\n{table_name} table content:')
        my_connection.query_table(table_name)
        my_connection.cursor.close()

    @staticmethod
    def find_duplicates():
        print('\nLog: looking for duplicates in sqlite database')
        duplicates = classDuplicates.sqliteDuplicates(rf'{classDB.sqlitedb_path}\\', 'publishing.db')
        duplicates.get_duplicates('News')
        duplicates.get_duplicates('PrivateAd')
        duplicates.get_duplicates('Horoscope')
        duplicates.cursor.close()
