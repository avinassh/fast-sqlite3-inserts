# fast-sqlite3-inserts

To find out the fastest way to create an SQLite DB with 1B random rows.

## Current Benchmark

```shell
$ ./bench.sh

Sat May  8 19:08:47 IST 2021 [PYTHON] running naive.py (10_000_000) inserts
      855.29 real       158.63 user       258.69 sys

Sat May  8 19:23:02 IST 2021 [PYTHON] running naive_batched.py (10_000_000) inserts
      569.71 real       114.91 user       252.70 sys

Sat May  8 19:32:32 IST 2021 [PYTHON] running sqlite3_opt.py (100_000_000) inserts
      609.06 real       603.59 user         3.55 sys

Sat May  8 19:42:44 IST 2021 [PYTHON] running sqlite3_opt_batched.py (100_000_000) inserts
      517.53 real       508.24 user         7.35 sys

Sat May  8 19:51:24 IST 2021 [PYTHON] running threaded_batched.py (100_000_000) inserts
      697.70 real       515.22 user       170.90 sys

Sat May  8 20:03:04 IST 2021 [PYPY] running sqlite3_opt_batched.py (100_000_000) inserts
      159.70 real       153.46 user         5.81 sys

Sat May  8 20:05:45 IST 2021 [PYPY] running threaded_batched.py (100_000_000) inserts
      324.12 real       224.14 user        84.69 sys
```