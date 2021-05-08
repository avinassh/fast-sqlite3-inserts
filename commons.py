"""all the common helper methods used by the Python script
"""
import random
import sqlite3


def create_table(con: sqlite3.Connection):
    con.execute("""
        create table IF NOT EXISTS user
        (
            id INTEGER not null primary key,
            area CHAR(6),
            age INTEGER not null,
            active INTEGER not null
        )
    """)


def get_random_area_code() -> str:
    return ''.join([F"{random.randint(0, 9)}" for _ in range(0, 6)])


def get_random_age() -> int:
    return random.choice([5, 10, 15])


def get_random_active() -> int:
    return 1 if get_random_bool() else 0


def get_random_bool() -> bool:
    return bool(random.getrandbits(1))
