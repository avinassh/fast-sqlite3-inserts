import sqlite3

from commons import get_random_age, get_random_active, get_random_bool, get_random_area_code, create_table

DB_NAME = "naive.db"


def faker(con: sqlite3.Connection, count=100_000):
    for _ in range(count):
        age = get_random_age()
        active = get_random_active()
        # switch for area code
        if get_random_bool():
            # random 6 digit number
            area = get_random_area_code()
            con.execute('INSERT INTO user VALUES (NULL,?,?,?)', (area, age, active))
        else:
            con.execute('INSERT INTO user VALUES (NULL,NULL,?,?)', (age, active))
        con.commit()


def main():
    con = sqlite3.connect(DB_NAME, isolation_level=None)
    con.execute('PRAGMA journal_mode = WAL;')
    create_table(con)
    faker(con, count=10_000_000)


if __name__ == '__main__':
    main()
