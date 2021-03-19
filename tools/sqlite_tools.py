import sqlite3


def list_db_table_names(sqlite_db):
    con = sqlite3.connect(sqlite_db)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    list_tables = cursor.fetchall()
    list_tables = [i[0] for i in list_tables]
    return list_tables


if __name__ == '__main__':
    print('sqlite tools')
