""" busy loop

This code does not really do anything, just runs two for loops. It has no SQL code. The idea was to measure how
much time python spending just to run a for loop, generating data.
"""

import sqlite3

from commons import get_random_age, get_random_active, get_random_bool, get_random_area_code, create_table


def faker(count=100_000):
    min_batch_size = 1_000_000
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


def main():
    faker(count=100_000_000)


if __name__ == '__main__':
    main()
