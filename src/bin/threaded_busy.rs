use std::thread;
extern crate num_cpus;

mod common;

fn faker(count: i64) {
    let min_batch_size = 1_000_000;
    for _ in 0..(count / min_batch_size) {
        let with_area = common::get_random_bool();
        let mut current_batch = Vec::<(String, i8, i8)>::new();
        for _ in 0..min_batch_size {
            if with_area {
                current_batch.push((
                    common::get_random_area_code(),
                    common::get_random_age(),
                    common::get_random_active(),
                ));
            } else {
                current_batch.push((
                    "".parse().unwrap(),
                    common::get_random_age(),
                    common::get_random_active(),
                ));
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
