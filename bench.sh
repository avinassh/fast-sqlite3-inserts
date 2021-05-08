# runs each of the scripts one after another, prints the measurements to stdout
export TZ=":Asia/Kolkata"

# benching naive version
rm -rf naive.db naive.db-shm naive.db-wal
echo "$(date)" "[PYTHON] running naive.py (10_000_000) inserts"
/usr/bin/time python3 naive.py
# lets verify the data exists
if [[ $(sqlite3 naive.db  "select count(*) from user";) = 10000000 ]]; then
  echo "data verified"
fi

# benching naive batched
rm -rf naive_batched.db naive_batched.db-shm naive_batched.db-wal
echo
echo "$(date)" "[PYTHON] running naive_batched.py (10_000_000) inserts"
/usr/bin/time python3 naive_batched.py
if [[ $(sqlite3 naive_batched.db  "select count(*) from user";) = 10000000 ]]; then
  echo "data verified"
fi
