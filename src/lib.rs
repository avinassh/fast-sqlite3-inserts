use once_cell::sync::Lazy;
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

pub fn get_random_area_code() -> &'static str {
    static AREA_CODES: Lazy<Vec<TinyStr8>> = Lazy::new(|| {
        (0..=999_999)
            .map(|i| TinyStr8::from_bytes(&format_6digits_number(i)).unwrap())
            .collect()
    });

    &AREA_CODES[fastrand::usize(0..=999_999)]
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
