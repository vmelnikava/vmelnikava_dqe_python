import pyodbc


class sqliteDuplicates:
    def __init__(self, path, database):
        connection_string = ('DRIVER={SQLite3 ODBC Driver};'
                             'Direct=True;'
                             f'DATABASE={path}\\{database};'
                             'String Types= Unicode')
        with pyodbc.connect(connection_string, autocommit=True) as self.connection:
            self.cursor = self.connection.cursor()

    def get_column_list(self, p_table):
        self.cursor.execute(f"select * from {p_table}")
        list_columns = list(map(lambda x: x[0], self.cursor.description))
        return ', '.join(list_columns)

    def get_duplicates(self, p_table):
        my_columns = self.get_column_list(p_table)
        self.cursor.execute(f"select count(*) as count, {my_columns} from {p_table} group by {my_columns} having "
                            f"count(*)>1")
        result = self.cursor.fetchall()
        if not result:
            print(f'No duplicates found in {p_table}')
        else:
            print(f'\nDuplicates found in {p_table}:')
            for row in result:
                print('row:', row[1:], '\ncount:', row.count)
