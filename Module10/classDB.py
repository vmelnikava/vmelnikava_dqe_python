import sqlite3

sqlitedb_path = 'D:\\Python_DQE\\Module10'


class DBConnection:
    def __init__(self, database_name):
        with sqlite3.connect(database_name) as self.connection:
            self.cursor = self.connection.cursor()

    def create_table(self, table_name, parameters):
        self.cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE name='{table_name}'")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute(f'CREATE TABLE {table_name}({parameters})')
            print(f"Log: table '{table_name}' has been created")

    def query_table(self, table_name):
        self.cursor.execute(f'select * from {table_name}')
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        return rows

    def insert_row(self, table_name, values):
        self.cursor.execute(f'INSERT INTO {table_name} VALUES {values}')
        return self.cursor.fetchall()

    def commit_changes(self):
        print('Log: committing')
        self.connection.commit()
