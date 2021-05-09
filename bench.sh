# runs each of the scripts one after another, prints the measurements to stdout
export TZ=":Asia/Kolkata"

# benching naive version
rm -rf naive.db naive.db-shm naive.db-wal
echo "$(date)" "[PYTHON] running naive.py (10_000_000) inserts"
/usr/bin/time python3 naive.py
# lets verify the data exists
if [[ $(sqlite3 naive.db  "select count(*) from user";) != 10000000 ]]; then
  echo "data verification failed"
fi

# benching naive batched
rm -rf naive_batched.db naive_batched.db-shm naive_batched.db-wal
echo
echo "$(date)" "[PYTHON] running naive_batched.py (10_000_000) inserts"
/usr/bin/time python3 naive_batched.py
if [[ $(sqlite3 naive_batched.db  "select count(*) from user";) != 10000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized
rm -rf sqlite3_opt.db sqlite3_opt.db-shm sqlite3_opt.db-wal
echo
echo "$(date)" "[PYTHON] running sqlite3_opt.py (100_000_000) inserts"
/usr/bin/time python3 sqlite3_opt.py
if [[ $(sqlite3 sqlite3_opt.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized and batched
rm -rf sqlite3_opt_batched.db sqlite3_opt_batched.db-shm sqlite3_opt_batched.db-wal
echo
echo "$(date)" "[PYTHON] running sqlite3_opt_batched.py (100_000_000) inserts"
/usr/bin/time python3 sqlite3_opt_batched.py
if [[ $(sqlite3 sqlite3_opt_batched.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized, batched and threaded
rm -rf threaded_batched.db threaded_batched.db-shm threaded_batched.db-wal
echo
echo "$(date)" "[PYTHON] running threaded_batched.py (100_000_000) inserts"
/usr/bin/time python3 threaded_batched.py
# this will fail anyways
if [[ $(sqlite3 threaded_batched.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized, batched, single threaded but on pypy
rm -rf sqlite3_opt_batched.db sqlite3_opt_batched.db-shm sqlite3_opt_batched.db-wal
echo
echo "$(date)" "[PYPY] running sqlite3_opt_batched.py (100_000_000) inserts"
/usr/bin/time pypy3 sqlite3_opt_batched.py
if [[ $(sqlite3 sqlite3_opt_batched.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching sqlite3 optimized, batched, threaded but on pypy
rm -rf threaded_batched.db threaded_batched.db-shm threaded_batched.db-wal
echo
echo "$(date)" "[PYPY] running threaded_batched.py (100_000_000) inserts"
/usr/bin/time pypy3 threaded_batched.py
# this will fail anyways
if [[ $(sqlite3 threaded_batched.db  "select count(*) from user";) != 100000000 ]]; then
  echo "data verification failed"
fi

# benching busy loop
echo
echo "$(date)" "[PYTHON] busy_loop.py (100_000_000) iterations"
/usr/bin/time python3 busy_loop.py
echo
echo "$(date)" "[PYPY] busy_loop.py (100_000_000) iterations"
/usr/bin/time pypy3 busy_loop.py
echo
cargo build --release --quiet --bin busy
echo "$(date)" "[RUST] busy.rs (100_000_000) iterations"
/usr/bin/time ./target/release/busy
echo
cargo build --release --quiet --bin threaded_busy
echo "$(date)" "[RUST] threaded_busy.rs (100_000_000) iterations"
/usr/bin/time ./target/release/threaded_busy
