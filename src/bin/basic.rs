//! naive version
//!
//! This is the first Rust version I came up with. This builds from the Python versions, so I have
//! included all the SQLite optimisations. However, there is no batching involved, I just have a
//! long for loop where it loops over 100M and inserts the rows one by one.
//!
//! next: basic_async.rs

use fast_sqlite3_inserts::*;
use rusqlite::{params, Connection};

fn faker(mut conn: Connection, count: i64) {
    let tx = conn.transaction().unwrap();
    for _ in 0..count {
        let with_area = get_random_bool();
        let age = get_random_age();
        let is_active = get_random_active();
        if with_area {
            let area_code = get_random_area_code();
            tx.execute(
                "INSERT INTO user VALUES (NULL, ?, ?, ?)",
                params![area_code, age, is_active],
            )
            .unwrap();
        } else {
            tx.execute(
                "INSERT INTO user VALUES (NULL, NULL, ?, ?)",
                params![age, is_active],
            )
            .unwrap();
        }
    }
    tx.commit().unwrap();
}

fn main() {
    let conn = Connection::open("basic.db").unwrap();
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
    faker(conn, 100_000_000)
}
