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
