//! busy loop but threaded.
//!
//! This code does not really do anything, just runs two for loops. It has no SQL code. The idea was to measure how much
//! time rust spending just to run a for loop, generating data. This builds upon busy.rs and uses multiple threads.
//!
//! previous: busy.rs

use std::thread;
extern crate num_cpus;

use crate::common::AreaCode;
use fast_sqlite3_inserts as common;

fn faker(count: i64) {
    let min_batch_size = 1_000_000;
    for _ in 0..(count / min_batch_size) {
        let with_area = common::get_random_bool();
        let mut current_batch = Vec::<(Option<AreaCode>, i8, i8)>::new();
        for _ in 0..min_batch_size {
            if with_area {
                current_batch.push((
                    Some(common::get_random_area_code()),
                    common::get_random_age(),
                    common::get_random_active(),
                ));
            } else {
                current_batch.push((None, common::get_random_age(), common::get_random_active()));
            }
        }
    }
}

fn multi_producers() {
    let cpu_count = num_cpus::get();
    let total_rows = 100_000_000;
    let each_producer_count = (total_rows / cpu_count) as i64;
    let mut handles = Vec::with_capacity(cpu_count);
    for _ in 0..cpu_count {
        handles.push(thread::spawn(move || faker(each_producer_count.clone())))
    }
    for t in handles {
        t.join().unwrap();
    }
}

fn main() {
    multi_producers()
}
