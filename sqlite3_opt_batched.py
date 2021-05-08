import sqlite3

from commons import get_random_age, get_random_active, get_random_bool, get_random_area_code, create_table

DB_NAME = "sqlite3_opt_batched.db"


def faker(con: sqlite3.Connection, count=100_000):
    min_batch_size = 1_00_000
    con.execute('BEGIN')
    for _ in range(int(count / min_batch_size)):
        with_area = get_random_bool()
        current_batch = []
        for _ in range(min_batch_size):
            age = get_random_age()
            active = get_random_active()
            # switch for area code
            if with_area:
                # random 6 digit number
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
    con.execute('PRAGMA journal_mode = OFF;')
    con.execute('PRAGMA synchronous = 0;')
    con.execute('PRAGMA cache_size = 1000000;')  # give it a GB
    con.execute('PRAGMA locking_mode = EXCLUSIVE;')
    con.execute('PRAGMA temp_store = MEMORY;')
    create_table(con)
    faker(con, count=100_000_000)


if __name__ == '__main__':
    main()
