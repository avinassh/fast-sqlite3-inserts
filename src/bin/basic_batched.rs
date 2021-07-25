//! batched and prepared statements
//!
//! This builds upon basic_prep, however we do batched insertions. Each batch is is of size 50.
//!
//! This is second fastest version in rust.
//!
//! previous: basic_prep.rs
//! next: basic_batched_wp.rs

use rusqlite::{Connection, ToSql, Transaction};
use rsor::Slice;

mod common;

fn faker_wrapper(mut conn: Connection, count: i64) {
    let tx = conn.transaction().unwrap();
    faker(&tx, count);
    tx.commit().unwrap();
}

fn faker(tx: &Transaction, count: i64) {
    // that is, we will batch 50 inserts of rows at once
    let min_batch_size: i64 = 50;
    if count < min_batch_size {
        panic!("count cant be less than min batch size");
    }

    // the way this works is
    // 1. we build a prepared statement and cache it so that it can be re-used. We build two of those
    // one for insertions with area and another for without area code.
    //
    // 2. Then we will build the parameters which can be passed to these prepared statements.
    // 3. Execute
    // 4. ???
    // 5. Profit

    // we will build parameters to pass to prepared statements
    // jeez, refactor this!
    let mut with_area_params = " (NULL, ?, ?, ?),".repeat(min_batch_size as usize);
    with_area_params.pop();
    let with_area_params = with_area_params.as_str();
    let mut without_area_params = " (NULL, NULL, ?, ?),".repeat(min_batch_size as usize);
    without_area_params.pop();
    let without_area_params = without_area_params.as_str();
    let st1 = format!("INSERT INTO user VALUES {}", with_area_params);
    let st2 = format!("INSERT INTO user VALUES {}", without_area_params);

    let mut stmt_with_area = tx.prepare_cached(st1.as_str()).unwrap();
    let mut stmt = tx.prepare_cached(st2.as_str()).unwrap();
    let mut params_with_area = Vec::with_capacity(min_batch_size as usize);
    let mut param_values = Slice::with_capacity(min_batch_size as usize * 3);
    for _ in 0..(count / min_batch_size) {
        let with_area = common::get_random_bool();
        let age = common::get_random_age();
        let is_active = common::get_random_active();
        if with_area {
            for _ in 0..min_batch_size {
                let area_code = common::get_random_area_code();
                params_with_area.push((area_code,));
            }
            let param_values = param_values.fill(|mut v| {
                for params in &params_with_area {
                    v.push(&params.0 as &dyn ToSql);
                    v.push(&age as &dyn ToSql);
                    v.push(&is_active as &dyn ToSql);
                }
                v
            });
            stmt_with_area.execute(&*param_values).unwrap();
            params_with_area.clear();
        } else {
            let param_values = param_values.fill(|mut v| {
                for _ in 0..min_batch_size {
                    v.push(&age as &dyn ToSql);
                    v.push(&is_active as &dyn ToSql);
                }
                v
            });
            stmt.execute(&*param_values).unwrap();
        }
    }
}

fn main() {
    let conn = Connection::open("basic_batched.db").unwrap();
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
