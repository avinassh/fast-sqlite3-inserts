//! naive but async version
//!
//! This is very similar to basic.rs, just that it is asynchronous. I also wanted to try out sqlx
//! and rest of all the examples are sync and uses rusqlite
//!
//! previous: basic.rs
//! next: basic_prep.rs

mod common;
    
#[cfg(feature = "async-sql")]
mod inline {
    use std::str::FromStr;
    use super::common;
    
    use sqlx::sqlite::{SqliteConnectOptions, SqliteJournalMode, SqliteSynchronous};
    use sqlx::{ConnectOptions, Connection, Executor, SqliteConnection, Statement};
    
    async fn faker(mut conn: SqliteConnection, count: i64) -> Result<(), sqlx::Error> {
        let mut tx = conn.begin().await?;
        let stmt_with_area = tx
            .prepare("INSERT INTO user VALUES (NULL, ?, ?, ?)")
            .await?;
        let stmt = tx
            .prepare("INSERT INTO user VALUES (NULL, NULL, ?, ?)")
            .await?;
        for _ in 0..count {
            let with_area = common::get_random_bool();
            let age = common::get_random_age();
            let is_active = common::get_random_active();
            if with_area {
                let area_code = common::get_random_area_code();
                stmt_with_area
                    .query()
                    .bind(area_code)
                    .bind(age)
                    .bind(is_active)
                    .execute(&mut tx)
                    .await?;
            } else {
                stmt.query()
                    .bind(age)
                    .bind(is_active)
                    .execute(&mut tx)
                    .await?;
            }
        }
        tx.commit().await?;
        Ok(())
    }
    
    #[tokio::main]
    pub async fn main() -> Result<(), sqlx::Error> {
        let mut conn = SqliteConnectOptions::from_str("basic_async.db")
            .unwrap()
            .create_if_missing(true)
            .journal_mode(SqliteJournalMode::Off)
            .synchronous(SqliteSynchronous::Off)
            .connect()
            .await?;
        conn.execute("PRAGMA cache_size = 1000000;").await?;
        conn.execute("PRAGMA locking_mode = EXCLUSIVE;").await?;
        conn.execute("PRAGMA temp_store = MEMORY;").await?;
        conn.execute(
            "CREATE TABLE IF NOT EXISTS user (
                    id INTEGER not null primary key,
                    area CHAR(6),
                    age INTEGER not null,
                    active INTEGER not null);",
        )
        .await?;
        faker(conn, 100_000_000).await?;
        Ok(())
    }
}

fn main() {
    #[cfg(feature = "async-sql")]
    inline::main().unwrap();
}
