#!/bin/sh
# runs each of the scripts one after another, prints the measurements to stdout
export TZ=":Asia/Kolkata"

# benching sqlite cli
rm -rf sqlite3.db
echo "$(date)" "[SQLite] running sqlite3 (100_000_000) inserts"
time sqlite3 sqlite3.db '.read schema.sql' '.read load.sql'
if [[ $(sqlite3 sqlite3.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching naive version
rm -rf naive.db naive.db-shm naive.db-wal
echo "$(date)" "[PYTHON] running naive.py (10_000_000) inserts"
time python3 naive.py
# lets verify the data exists
if [[ $(sqlite3 naive.db  "select count(*) from user";) != 10000000 ]]; then
  echo "data verification failed"
fi

# benching naive batched
rm -rf naive_batched.db naive_batched.db-shm naive_batched.db-wal
echo
echo "$(date)" "[PYTHON] running naive_batched.py (10_000_000) inserts"
time python3 naive_batched.py
if [[ $(sqlite3 naive_batched.db  "select count(*) from user";) != 10000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized
rm -rf sqlite3_opt.db sqlite3_opt.db-shm sqlite3_opt.db-wal
echo
echo "$(date)" "[PYTHON] running sqlite3_opt.py (100_000_000) inserts"
time python3 sqlite3_opt.py
if [[ $(sqlite3 sqlite3_opt.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized on PYPY
rm -rf sqlite3_opt.db sqlite3_opt.db-shm sqlite3_opt.db-wal
echo
echo "$(date)" "[PYPY] running sqlite3_opt.py (100_000_000) inserts"
time pypy3 sqlite3_opt.py
if [[ $(sqlite3 sqlite3_opt.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized and batched
rm -rf sqlite3_opt_batched.db sqlite3_opt_batched.db-shm sqlite3_opt_batched.db-wal
echo
echo "$(date)" "[PYTHON] running sqlite3_opt_batched.py (100_000_000) inserts"
time python3 sqlite3_opt_batched.py
if [[ $(sqlite3 sqlite3_opt_batched.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized, batched and threaded
rm -rf threaded_batched.db threaded_batched.db-shm threaded_batched.db-wal
echo
echo "$(date)" "[PYTHON] running threaded_batched.py (100_000_000) inserts"
time python3 threaded_batched.py
# this will fail anyways
if [[ $(sqlite3 threaded_batched.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized, batched, single threaded but on pypy
rm -rf sqlite3_opt_batched.db sqlite3_opt_batched.db-shm sqlite3_opt_batched.db-wal
echo
echo "$(date)" "[PYPY] running sqlite3_opt_batched.py (100_000_000) inserts"
time pypy3 sqlite3_opt_batched.py
if [[ $(sqlite3 sqlite3_opt_batched.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized, batched, threaded but on pypy
rm -rf threaded_batched.db threaded_batched.db-shm threaded_batched.db-wal
echo
echo "$(date)" "[PYPY] running threaded_batched.py (100_000_000) inserts"
time pypy3 threaded_batched.py
# this will fail anyways
if [[ $(sqlite3 threaded_batched.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching with all prev sqlite optimisations, but on rust with sqlx async
rm -rf basic_async.db basic_async.db-shm basic_async.db-wal
cargo build --release --quiet --bin basic_async
echo "$(date)" "[RUST] basic_async.rs (100_000_000) inserts"
time ./target/release/basic_async

# benching with all prev sqlite optimisations, but on rust with rusqlite
rm -rf basic.db basic.db-shm basic.db-wal
cargo build --release --quiet --bin basic
echo "$(date)" "[RUST] basic.rs (100_000_000) inserts"
time ./target/release/basic

# benching with all prev sqlite optimisations, but on rust with rusqlite with batched inserts where
# each batch is a really large ass string
rm -rf basic_batched_wp.db basic_batched_wp.db-shm basic_batched_wp.db-wal
cargo build --release --quiet --bin basic_batched_wp
echo "$(date)" "[RUST] basic_batched_wp.rs (100_000_000) inserts"
time ./target/release/basic_batched_wp

# just like the previous version, so really bad.
rm -rf threaded_str_batched.db threaded_str_batched.db-shm threaded_str_batched.db-wal
cargo build --release --quiet --bin threaded_str_batched
echo "$(date)" "[RUST] threaded_str_batched.rs (100_000_000) inserts"
time ./target/release/threaded_str_batched


# benching with all prev sqlite optimisations, but on rust with rusqlite with inserts where
# each batch is a proper prepared statement
rm -rf basic_prep.db basic_prep.db-shm basic_prep.db-wal
cargo build --release --quiet --bin basic_prep
echo "$(date)" "[RUST] basic_prep.rs (100_000_000) inserts"
time ./target/release/basic_prep

# benching with all prev sqlite optimisations, but on rust with rusqlite with batched inserts where
# each batch is a proper prepared statement
rm -rf basic_batched.db basic_batched.db-shm basic_batched.db-wal
cargo build --release --quiet --bin basic_batched
echo "$(date)" "[RUST] basic_batched.rs (100_000_000) inserts"
time ./target/release/basic_batched

# previous version but threaded
rm -rf threaded_batched.db threaded_batched.db-shm threaded_batched.db-wal
cargo build --release --quiet --bin threaded_batched
echo "$(date)" "[RUST] threaded_batched.rs (100_000_000) inserts"
time ./target/release/threaded_batched
