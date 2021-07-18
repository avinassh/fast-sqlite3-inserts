//! prepared statements
//!
//! This is very similar to basic.rs, just that it uses prepared statements. We have a long for loop
//! of 100M and insert each row one by one.
//!
//! previous: basic_async.rs
//! next: basic_batched.rs

use rusqlite::{params, Connection, Transaction};

mod common;

fn faker_wrapper(mut conn: Connection, count: i64) {
    let tx = conn.transaction().unwrap();
    faker(&tx, count);
    tx.commit().unwrap();
}

fn faker(tx: &Transaction, count: i64) {
    let mut stmt_with_area = tx
        .prepare_cached("INSERT INTO user VALUES (?, ?, ?, ?)")
        .unwrap();
    let mut stmt = tx
        .prepare_cached("INSERT INTO user VALUES (?, NULL, ?, ?)")
        .unwrap();
    let mut pk: i64 = 1;
    for _ in 0..count {
        let with_area = common::get_random_bool();
        let age = common::get_random_age();
        let is_active = common::get_random_active();
        if with_area {
            let area_code = common::get_random_area_code();
            stmt_with_area
                .execute(params![pk, area_code, age, is_active])
                .unwrap();
        } else {
            stmt.execute(params![pk, age, is_active]).unwrap();
        }
        pk += 1;
    }
}

fn main() {
    let conn = Connection::open("basic_prep.db").unwrap();
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
    faker_wrapper(conn, 100_000_000)
}
