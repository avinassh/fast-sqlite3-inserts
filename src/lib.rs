use rusqlite::{types::ToSqlOutput, ToSql};
use tinystr::TinyStr8;

pub fn get_random_age() -> i8 {
    [5, 10, 15][fastrand::usize(0..3)]
}

pub fn get_random_active() -> i8 {
    fastrand::bool().into()
}

pub fn get_random_bool() -> bool {
    fastrand::bool()
}

pub fn get_random_area_code() -> AreaCode {
    let n = fastrand::u32(0..=999_999);
    let buffer = format_6digits_number(n);
    TinyStr8::from_bytes(&buffer).map(AreaCode).unwrap()
}

/// Formats a number that is between 0 and 999_999,
/// the number will be padded with `0`s.
pub fn format_6digits_number(mut n: u32) -> [u8; 6] {
    let mut buffer = [b'0'; 6];
    let mut i = buffer.len() - 1;
    while i < buffer.len() {
        buffer[i] = (n % 10) as u8 + b'0';
        n = n / 10;
        i = i.wrapping_sub(1);
    }
    buffer
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn formatting() {
        for n in 0..=999_999 {
            let output = format_6digits_number(n);
            let expected = format!("{:06}", n);
            assert_eq!(output, expected.as_bytes());
        }
    }
}

pub struct AreaCode(TinyStr8);

impl AreaCode {
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

impl ToSql for AreaCode {
    fn to_sql(&self) -> rusqlite::Result<ToSqlOutput<'_>> {
        Ok(ToSqlOutput::from(self.0.as_str()))
    }
}
