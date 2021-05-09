use std::env;
use std::str::FromStr;

use sqlx::sqlite::{SqliteConnectOptions, SqliteJournalMode, SqliteSynchronous};
use sqlx::{ConnectOptions, Connection, Executor, SqliteConnection};

mod common;

async fn faker(mut conn: SqliteConnection, count: i64) -> Result<(), sqlx::Error> {
    let mut tx = conn.begin().await?;
    for _ in 0..count {
        let with_area = common::get_random_bool();
        let age = common::get_random_age();
        let is_active = common::get_random_active();
        if with_area {
            let area_code = common::get_random_area_code();
            sqlx::query!(
                r#"INSERT INTO user VALUES ( NULL, ?1, ?2, ?3 )"#,
                area_code,
                age,
                is_active
            )
            .execute(&mut tx)
            .await?;
        } else {
            sqlx::query!(
                r#"INSERT INTO user VALUES ( NULL, NULL, ?1, ?2 )"#,
                age,
                is_active
            )
            .execute(&mut tx)
            .await?;
        }
    }
    tx.commit().await?;
    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    let mut conn = SqliteConnectOptions::from_str(&env::var("DATABASE_URL").unwrap())?
        .journal_mode(SqliteJournalMode::Off)
        .synchronous(SqliteSynchronous::Off)
        .connect()
        .await?;
    conn.execute("PRAGMA cache_size = 1000000;").await?;
    conn.execute("PRAGMA locking_mode = EXCLUSIVE;").await?;
    conn.execute("PRAGMA temp_store = MEMORY;").await?;

    faker(conn, 100_000_000).await?;

    Ok(())
}
