//! batched, prepared statements and also threaded
//!
//! This builds upon basic_batched version and very similar to the python counterpart `threaded_batched.py`
//!
//! We have a channel, spawn a single writer thread which consumes from queue and writes to SQLite.
//! Then we spawn few more producer threads which generate the data, push to channel.
//!
//! previous: basic_batched.rs
//! next: threaded_str_batched.rs

use fast_sqlite3_inserts::*;

use rusqlite::{Connection, ToSql};
use std::sync::mpsc;
use std::sync::mpsc::{Receiver, Sender};
use std::thread;

static MIN_BATCH_SIZE: i64 = 50;

enum ParamValues {
    WithArea(Vec<(String, i8, i8)>),
    WithoutArea(Vec<(i8, i8)>),
}

fn consumer(rx: Receiver<ParamValues>) {
    let mut conn = Connection::open("threaded_batched.db").unwrap();
    conn.execute_batch(
        "PRAGMA journal_mode = OFF;
              PRAGMA synchronous = 0;
              PRAGMA cache_size = 1000000;
              PRAGMA locking_mode = EXCLUSIVE;
              PRAGMA temp_store = MEMORY;",
    )
    .expect("PRAGMA");
    conn.execute(
        "CREATE TABLE IF NOT EXISTS user (
                id INTEGER not null primary key,
                area CHAR(6),
                age INTEGER not null,
                active INTEGER not null)",
        [],
    )
    .unwrap();
    let tx = conn.transaction().unwrap();
    {
        // TODO: refactor and DRY from basic_batched
        // jeez, refactor this!
        // this is very similar to the code from basic_batched, check that file to understand
        // whats happening here.
        let mut with_area_params = " (NULL, ?, ?, ?),".repeat(MIN_BATCH_SIZE as usize);
        with_area_params.pop();
        let with_area_params = with_area_params.as_str();
        let mut without_area_params = " (NULL, NULL, ?, ?),".repeat(MIN_BATCH_SIZE as usize);
        without_area_params.pop();
        let without_area_params = without_area_params.as_str();
        let st1 = format!("INSERT INTO user VALUES {}", with_area_params);
        let st2 = format!("INSERT INTO user VALUES {}", without_area_params);

        let mut stmt_with_area = tx.prepare_cached(st1.as_str()).unwrap();
        let mut stmt_without_area = tx.prepare_cached(st2.as_str()).unwrap();
        for param_values in rx {
            let mut row_values: Vec<&dyn ToSql> = Vec::new();
            match param_values {
                ParamValues::WithArea(values) => {
                    for batch in values.iter() {
                        row_values.push(&batch.0 as &dyn ToSql);
                        row_values.push(&batch.1 as &dyn ToSql);
                        row_values.push(&batch.2 as &dyn ToSql);
                    }
                    stmt_with_area.execute(&*row_values).unwrap();
                }
                ParamValues::WithoutArea(values) => {
                    for batch in values.iter() {
                        row_values.push(&batch.0 as &dyn ToSql);
                        row_values.push(&batch.1 as &dyn ToSql);
                    }
                    stmt_without_area.execute(&*row_values).unwrap();
                }
            }
        }
    }
    tx.commit().unwrap();
}

fn producer(tx: Sender<ParamValues>, count: i64) {
    if count < MIN_BATCH_SIZE {
        panic!("count cant be less than min batch size");
    }
    for _ in 0..(count / MIN_BATCH_SIZE) {
        let with_area = get_random_bool();
        let age = get_random_age();
        let is_active = get_random_active();
        let mut param_values: Vec<_> = Vec::new();
        if with_area {
            // lets prepare the batch
            let mut vector = Vec::<(String, i8, i8)>::new();
            for _ in 0..MIN_BATCH_SIZE {
                let area_code = get_random_area_code();
                vector.push((area_code, age, is_active));
            }
            for batch in vector.iter() {
                param_values.push(&batch.0 as &dyn ToSql);
                param_values.push(&batch.1 as &dyn ToSql);
                param_values.push(&batch.2 as &dyn ToSql);
            }
            // send the values
            tx.send(ParamValues::WithArea(vector)).unwrap();
        } else {
            // lets prepare the batch
            let mut vector = Vec::<(i8, i8)>::new();
            for _ in 0..MIN_BATCH_SIZE {
                vector.push((age, is_active));
            }
            for batch in vector.iter() {
                param_values.push(&batch.0 as &dyn ToSql);
                param_values.push(&batch.1 as &dyn ToSql);
            }
            // send the values
            tx.send(ParamValues::WithoutArea(vector)).unwrap();
        }
    }
}

fn main() {
    // setup the DB and tables
    let (tx, rx): (Sender<ParamValues>, Receiver<ParamValues>) = mpsc::channel();
    // lets launch the consumer
    let consumer_handle = thread::spawn(|| consumer(rx));

    let cpu_count = num_cpus::get();
    let total_rows = 100_000_000;
    let each_producer_count = (total_rows / cpu_count) as i64;
    let mut handles = Vec::with_capacity(cpu_count);
    for _ in 0..cpu_count {
        let thread_tx = tx.clone();
        handles.push(thread::spawn(move || {
            producer(thread_tx, each_producer_count.clone())
        }))
    }
    for t in handles {
        t.join().unwrap();
    }
    drop(tx);
    // wait till consumer is exited
    consumer_handle.join().unwrap();
}
