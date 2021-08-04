//! busy loop
//!
//! This code does not really do anything, just runs two for loops. It has no SQL code. The idea was to measure how much 
//! time rust spending just to run a for loop, generating data.
//!
//! next: threaded_busy.rs

use fast_sqlite3_inserts::*;

fn faker(count: i64) {
    let min_batch_size = 1_000_000;
    for _ in 0..(count / min_batch_size) {
        let with_area = get_random_bool();
        let mut current_batch = Vec::<(String, i8, i8)>::new();
        for _ in 0..min_batch_size {
            if with_area {
                current_batch.push((
                    get_random_area_code(),
                    get_random_age(),
                    get_random_active(),
                ));
            } else {
                current_batch.push((
                    "".parse().unwrap(),
                    get_random_age(),
                    get_random_active(),
                ));
            }
        }
    }
}

fn main() {
    faker(100_000_000);
}
