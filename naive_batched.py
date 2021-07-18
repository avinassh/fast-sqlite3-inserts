""" naive batched

This version builds from naive.py, here I added batching. So instead of one 10M for loop, here we insert rows in a batches of 
100K. This has no SQLite optimisations either.

previous: naive.py
next: sqlite3_opt.py
"""

import sqlite3

from commons import get_random_age, get_random_active, get_random_bool, get_random_area_code, create_table

DB_NAME = "naive_batched.db"


def faker(con: sqlite3.Connection, count=100_000):
    min_batch_size = 1_00_000
    for _ in range(int(count / min_batch_size)):
        with_area = get_random_bool()
        current_batch = []
        for _ in range(min_batch_size):
            age = get_random_age()
            active = get_random_active()
            if with_area:
                area = get_random_area_code()
                current_batch.append((area, age, active))
            else:
                current_batch.append((age, active))

        if with_area:
            con.executemany('INSERT INTO user VALUES (NULL,?,?,?)', current_batch)
        else:
            con.executemany('INSERT INTO user VALUES (NULL,NULL,?,?)', current_batch)
        con.commit()


def main():
    con = sqlite3.connect(DB_NAME, isolation_level=None)
    con.execute('PRAGMA journal_mode = WAL;')
    create_table(con)
    faker(con, count=10_000_000)


if __name__ == '__main__':
    main()
