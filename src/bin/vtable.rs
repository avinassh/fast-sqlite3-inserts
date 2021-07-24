use std::os::raw::c_int;
use std::marker::PhantomData;
use std::mem::MaybeUninit;
use std::str::from_utf8_unchecked;

use rusqlite::{Connection, Result, Error, params};
use rusqlite::vtab::{
    Context, Values,
    VTab, VTabConnection, IndexInfo, sqlite3_vtab,
    VTabCursor, sqlite3_vtab_cursor,
    eponymous_only_module,
};

mod common;

#[repr(C)]
struct RandVTable {
    /// Base class. Must be first
    base: sqlite3_vtab,
    /* Virtual table implementations will typically add additional fields */
}
impl RandVTable {
    fn register(conn: &Connection) -> Result<()> {
        conn.create_module(
            "rand_vtab",
            eponymous_only_module::<'_, Self>(),
            None
        )
    }
}
unsafe impl<'vtab> VTab<'vtab> for RandVTable {
    type Aux = ();
    type Cursor = RandVTableCursor<'vtab>;

    fn connect(
        _db: &mut VTabConnection, 
        _aux: Option<&Self::Aux>, 
        _args: &[&[u8]]
    ) -> Result<(String, Self)> {
        Ok((
            "CREATE TABLE user (
                area CHAR(6),
                age INTEGER not null,
                active INTEGER not null
            )".to_owned(),
            Self { base: Default::default() }
        ))
    }

    fn best_index(&self, info: &mut IndexInfo) -> Result<()> {
        for i in 0..info.constraints().count() {
            let mut index_constraint_usage = info.constraint_usage(i);
            // no need of constrain in `<RandVTableCursor as VTabCursor>::filter`.
            index_constraint_usage.set_argv_index(0);
            // VTabCursor does not test for constrain, so sqlite3 must not
            // omit the test.
            index_constraint_usage.set_omit(false);
        }
        // RandVTable does not return ordered rows
        info.set_order_by_consumed(false);

        // idx_num is unused
        info.set_idx_num(0);

        // RandVTable has infinite tables
        let estimated_rows = i64::MAX;
        //info.set_estimated_rows(estimated_rows);

        // estimated_cost is linear
        info.set_estimated_cost(estimated_rows as f64);

        Ok(())
    }

    fn open(&'vtab self) -> Result<Self::Cursor> {
        Ok(Self::Cursor::new())
    }
}

#[repr(C)]
struct RandVTableCursor<'vtab> {
    /// Base class. Must be first
    base: sqlite3_vtab_cursor,
    /* Virtual table implementations will typically add additional fields */
    phantom: PhantomData<&'vtab RandVTable>,

    rowid: u64,

    area_code: [u8; 6],
    age: i8,
    active: i8,
}
impl<'vtab> RandVTableCursor<'vtab> {
    fn new() -> Self {
        Self {
            base: unsafe { MaybeUninit::zeroed().assume_init() },
            phantom: PhantomData,
            rowid: 0,
            area_code: common::get_random_area_code_u8(),
            age: common::get_random_age(),
            active: common::get_random_active(),
        }
    }
}
unsafe impl<'vtab> VTabCursor for RandVTableCursor<'vtab> {
    /// RandVTableCursor doesn't need any filter capacity
    fn filter(
        &mut self, 
        _idx_num: c_int, 
        _idx_str: Option<&str>, 
        _args: &Values<'_>
    ) -> Result<()> {
        Ok(())
    }

    fn next(&mut self) -> Result<()> {
        self.rowid += 1;

        self.area_code = common::get_random_area_code_u8();
        self.age       = common::get_random_age();
        self.active    = common::get_random_active();

        Ok(())
    }

    /// RandVTableCursor is endless
    fn eof(&self) -> bool {
        false
    }

    fn column(&self, ctx: &mut Context, i: c_int) -> Result<()> {
        match i {
            0 => ctx.set_result(unsafe { &from_utf8_unchecked(&self.area_code) })?,
            1 => ctx.set_result(&self.age)?,
            2 => ctx.set_result(&self.active)?,
            _ => return Err(Error::InvalidColumnIndex(i as usize)),
        };
        Ok(())
    }

    fn rowid(&self) -> Result<i64> {
        Ok(self.rowid as i64)
    }
}

fn faker(mut conn: Connection, count: i64) {
    let tx = conn.transaction().unwrap();
    tx.execute(
        "INSERT INTO user(area, age, active)
            SELECT * FROM rand_vtab LIMIT ?",
        params![count],
    ).unwrap();
    tx.commit().unwrap();
}


fn main() {
    let conn = Connection::open("vtable.db").unwrap();
    conn.execute(
        "CREATE TABLE IF NOT EXISTS user (
            id INTEGER not null primary key,
            area CHAR(6),
            age INTEGER not null,
            active INTEGER not null
        )",
        [],
    ).unwrap();

    RandVTable::register(&conn).unwrap();

    faker(conn, 100_000_000)
}
