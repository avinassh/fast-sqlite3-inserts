use rusqlite::Connection;
use std::sync::mpsc;
use std::sync::mpsc::{Receiver, Sender};
use std::thread;

mod common;

fn consumer(rx: Receiver<String>) {
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
    for stmt in rx {
        tx.execute(&*stmt, []).unwrap();
    }
    tx.commit().unwrap();
}

fn producer(tx: Sender<String>, count: i64) {
    let min_batch_size = 1_000_000;
    for _ in 0..(count / min_batch_size) {
        let mut stmt = "INSERT INTO user VALUES".to_owned();
        let with_area = common::get_random_bool();
        let age = common::get_random_age();
        let is_active = common::get_random_active();
        for _ in 0..min_batch_size {
            if with_area {
                let area_code = common::get_random_area_code();
                let params = format!(" (NULL, {}, {}, {}),", area_code, age, is_active);
                stmt.push_str(&params);
            } else {
                let params = format!(" (NULL, NULL, {}, {}),", age, is_active);
                stmt.push_str(&params);
            }
        }
        // at the end, we end up a with string which looks like:
        //
        // INSERT INTO user VALUES (NULL, NULL, 5, 1), (NULL, 1, 5, 1), (NULL, 1, 5, 1),
        //
        // Notice the `,` at the, which we will replace it with `;`
        stmt.pop();
        stmt.push(';');
        tx.send(stmt).unwrap();
    }
}

fn main() {
    let (tx, rx): (Sender<String>, Receiver<String>) = mpsc::channel();

    // lets launch the consumer
    let consumer_handle = thread::spawn(move || consumer(rx));

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
