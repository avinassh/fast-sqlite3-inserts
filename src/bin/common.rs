use fastrand;

pub fn get_random_age() -> i8 {
    [5, 10, 15][fastrand::usize(0..3)]
}

pub fn get_random_active() -> i8 {
    fastrand::bool().into()
}

pub fn get_random_bool() -> bool {
    fastrand::bool()
}

pub fn get_random_area_code() -> String {
    format!("{:06}", fastrand::u32(0..999_999))
}
