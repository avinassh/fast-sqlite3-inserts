use sqlx::Executor;
use sqlx::{Connection, SqliteConnection};

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    let mut conn = SqliteConnection::connect("sqlite::memory:").await?;
    conn.execute("PRAGMA journal_mode = OFF;").await?;
    Ok(())
}
