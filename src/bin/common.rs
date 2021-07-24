use rand::prelude::SliceRandom;
use rand::Rng;

pub fn get_random_age() -> i8 {
    let vs: Vec<i8> = vec![5, 10, 15];
    *vs.choose(&mut rand::thread_rng()).unwrap()
}

pub fn get_random_active() -> i8 {
    if rand::random() {
        return 1;
    }
    0
}

pub fn get_random_bool() -> bool {
    rand::random()
}

pub fn get_random_area_code() -> String {
    let mut rng = rand::thread_rng();
    format!("{:06}", rng.gen_range(0..999999))
}

pub fn get_random_area_code_u8() -> [u8; 6] {
    let mut rng = rand::thread_rng();

    let mut ret: [u8; 6] = Default::default();
    for each in &mut ret {
        *each = b'0' + rng.gen_range(0..9);
    }

    ret
}

pub fn get_random_optional_area_code_u8() -> Option<[u8; 6]> {
    if get_random_bool() {
        Some(get_random_area_code_u8())
    } else {
        None
    }
}
