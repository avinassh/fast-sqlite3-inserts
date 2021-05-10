use rusqlite::{Connection, ToSql, Transaction};

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
    for _ in 0..(count / min_batch_size) {
        let with_area = common::get_random_bool();
        let age = common::get_random_age();
        let is_active = common::get_random_active();
        let mut param_values: Vec<_> = Vec::new();
        if with_area {
            // lets prepare the batch
            let mut vector = Vec::<(String, i8, i8)>::new();
            for _ in 0..min_batch_size {
                let area_code = common::get_random_area_code();
                vector.push((area_code, age, is_active));
            }
            for batch in vector.iter() {
                param_values.push(&batch.0 as &dyn ToSql);
                param_values.push(&batch.1 as &dyn ToSql);
                param_values.push(&batch.2 as &dyn ToSql);
            }
            stmt_with_area.execute(&*param_values).unwrap();
        } else {
            // lets prepare the batch
            let mut vector = Vec::<(i8, i8)>::new();
            for _ in 0..min_batch_size {
                vector.push((age, is_active));
            }
            for batch in vector.iter() {
                param_values.push(&batch.0 as &dyn ToSql);
                param_values.push(&batch.1 as &dyn ToSql);
            }
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
