import queue
import sqlite3
import threading
import multiprocessing
from typing import List

from commons import get_random_age, get_random_active, get_random_bool, get_random_area_code, create_table

DB_NAME = "threaded_batch.db"

q = queue.Queue()


def consumer():
    con = sqlite3.connect(DB_NAME, isolation_level=None)
    con.execute('PRAGMA journal_mode = OFF;')
    con.execute('PRAGMA synchronous = 0;')
    con.execute('PRAGMA cache_size = 1000000;')  # give it a GB
    con.execute('PRAGMA locking_mode = EXCLUSIVE;')
    con.execute('PRAGMA temp_store = MEMORY;')
    create_table(con)

    while True:
        item = q.get()
        stmt, batch = item
        con.execute('BEGIN')
        con.executemany(stmt, batch)
        con.commit()
        q.task_done()


def producer(count: int):
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
        if with_area:
            q.put(('INSERT INTO user VALUES (NULL,?,?,?)', current_batch))
        else:
            q.put(('INSERT INTO user VALUES (NULL,NULL,?,?)', current_batch))


def main():
    total_rows = 100_000_000
    # start the consumer
    threading.Thread(target=consumer, daemon=True).start()

    # we would want to launch as many as producers, so we will take the max CPU value
    # and launch as many. We keep two threads, one for main and one for consumer.
    max_producers = multiprocessing.cpu_count() - 2

    # how many rows each producer should produce
    each_producer_count = int(total_rows / max_producers)

    producer_threads: List[threading.Thread] = [threading.Thread(
        target=producer, args=(each_producer_count,)) for _ in range(max_producers)]

    for p in producer_threads:
        p.start()

    for p in producer_threads:
        p.join()

    q.join()


if __name__ == '__main__':
    main()
