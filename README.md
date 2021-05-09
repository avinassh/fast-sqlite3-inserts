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

### Busy loop time
```
$ ./busy.sh

Sun May  9 13:16:01 IST 2021 [PYTHON] busy_loop.py (100_000_000) iterations
      351.14 real       347.53 user         3.39 sys

Sun May  9 13:21:52 IST 2021 [PYPY] busy_loop.py (100_000_000) iterations
       81.58 real        77.73 user         3.80 sys

Sun May  9 13:23:14 IST 2021 [RUST] busy.rs (100_000_000) iterations
       17.97 real        16.29 user         1.67 sys

Sun May  9 13:23:32 IST 2021 [RUST] threaded_busy.rs (100_000_000) iterations
        7.18 real        42.52 user         7.20 sys
```

### Rust

```
Sun May  9 15:40:13 IST 2021 [RUST] basic_async.rs (100_000_000) inserts
      814.85 real      1194.27 user       250.81 sys
```
