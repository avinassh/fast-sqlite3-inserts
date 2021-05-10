# runs each of the scripts one after another, prints the measurements to stdout
.SILENT:

export TZ := ":Asia/Kolkata"

busy-python:
	echo
	echo "$$(date)" "[PYTHON] busy_loop.py (100_000_000) iterations"
	/usr/bin/time python3 busy_loop.py

busy-pypy:
	echo
	echo "$$(date)" "[PYPY] busy_loop.py (100_000_000) iterations"
	/usr/bin/time pypy3 busy_loop.py

busy-rust:
	cargo build --release --quiet --bin busy
	echo
	echo "$$(date)" "[RUST] busy.rs (100_000_000) iterations"
	/usr/bin/time ./target/release/busy

busy-rust-thread:
	cargo build --release --quiet --bin threaded_busy
	echo
	echo "$$(date)" "[RUST] threaded_busy.rs (100_000_000) iterations"
	/usr/bin/time ./target/release/threaded_busy

busy-py-all: busy-python busy-pypy

busy-rust-all: busy-rust busy-rust-thread

busy-all: busy-py-all busy-rust-all
	