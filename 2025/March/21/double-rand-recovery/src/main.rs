extern crate mersenne_twister;
extern crate rand;
extern crate libc;
use mersenne_twister::MersenneTwister;
use rand::{Rng, SeedableRng};
use libc::{c_int, time_t, srand, rand, time};
use std::{time::{SystemTime, UNIX_EPOCH}, io::{self, Write}};
use chrono::{DateTime, Utc, TimeZone, NaiveDateTime};

// debug:
use std::thread;
use std::time::Duration;


fn try_time(timestamp: u32) -> Result<String, String> {
    // Load the encrypted data
    let encrypted_data = match std::fs::read_to_string("encrypted.txt") {
        Ok(content) => content
            .split(',')
            .filter_map(|s| s.trim().parse::<u32>().ok())
            .collect::<Vec<u32>>(),
        Err(_) => return Err("Failed to read encrypted.txt".to_string()),
    };
    
    if encrypted_data.len() <= 1000 + 12 {
        return Err("Encrypted data not long enough".to_string());
    }

    // Generate the first 1000 random values using the time-seeded rand
    let rand_values = unsafe {
        // Seed the random generator with this timestamp
        srand(timestamp);
        
        // Generate 1000 random values
        let mut values = Vec::with_capacity(1000);
        for _ in 0..1000 {
            values.push(rand() as u32);
        }
        values
    };

    // The first 624 values in the encrypted data are the XOR of rand_values and the original MT output
    // We can recover those original MT outputs
    let mut mt_samples = Vec::with_capacity(624);
    for i in 0..624 {
        mt_samples.push(encrypted_data[i] ^ rand_values[i]);
    }

    // Try to recover the MT state that would have generated those values
    let recovered_mt = mersenne_twister::MT19937::recover(&mt_samples);
    
    // Now, we need to generate the MT values that would have been used for positions 624 to 1000+12
    // The flag is at position 1000, and we think it's 12 words long
    
    // First, generate the values for positions 624 to 999 - these were used in the encryption
    // but aren't part of the flag
    let mut mt_clone = recovered_mt;
    let mut mt_values = Vec::with_capacity(400); // Enough to reach the flag region
    
    // We already have the first 624 values in mt_samples, so we only need to generate
    // values for indices 624 up to 1000+12
    for _ in 624..1000+12 {
        mt_values.push(mt_clone.next_u32());
    }
    
    // Now decrypt the flag at position 1000
    let flag_offset = 1000;
    let flag_length = 12;
    
    let mut flag_bytes = Vec::with_capacity(flag_length * 4);
    for i in 0..flag_length {
        // For indices >= 1000, we XOR with mt_values[i-624] since our mt_values array 
        // starts at index 624
        let mt_index = i + flag_offset - 624;
        if mt_index >= mt_values.len() {
            break;
        }
        
        let decrypted_word = encrypted_data[flag_offset + i] ^ mt_values[mt_index];
        
        // Convert each u32 to 4 bytes
        flag_bytes.push((decrypted_word & 0xFF) as u8);
        flag_bytes.push(((decrypted_word >> 8) & 0xFF) as u8);
        flag_bytes.push(((decrypted_word >> 16) & 0xFF) as u8);
        flag_bytes.push(((decrypted_word >> 24) & 0xFF) as u8);
    }
    
    // Try different ways of interpreting the bytes
    
    // Method 1: Take all bytes as-is
    if let Ok(flag) = String::from_utf8(flag_bytes.clone()) {
        if flag.contains("{") && flag.contains("}") {
            return Ok(flag);
        }
    }
    
    // Method 2: Take bytes until null terminator
    let flag_string: String = flag_bytes.iter()
        .take_while(|&&b| b != 0)
        .map(|&b| b as char)
        .collect();
    
    if flag_string.contains("{") && flag_string.contains("}") {
        return Ok(flag_string);
    }
    
    // Method 3: Only printable characters
    let printable_flag: String = flag_bytes.iter()
        .filter(|&&b| b >= 32 && b <= 126)
        .map(|&b| b as char)
        .collect();
    
    if printable_flag.contains("{") && printable_flag.contains("}") {
        return Ok(printable_flag);
    }
    
    Err("No valid flag found".to_string())
}

fn is_valid_flag(flag: &str) -> bool {
    flag.contains("ictf{")
}


fn main() {
    // Get current time as Unix timestamp
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards")
        .as_secs();
    unsafe {
        // Get current time as Unix timestamp (seconds since January 1, 1970)
        let current_time: time_t = time(std::ptr::null_mut());
        println!("Current C Unix timestamp: {}", current_time);
    }
    println!("Current Unix timestamp: {}", now);
    
    // Convert Unix timestamp to human-readable format using chrono
    let datetime = Utc.timestamp_opt(now as i64, 0).unwrap();
    println!("Current time: {}", datetime.format("%Y-%m-%d %H:%M:%S"));
    
    // Convert a specific timestamp to human-readable format
    let specific_time = 1742576400; // Your example timestamp
    let specific_datetime = Utc.timestamp_opt(specific_time, 0).unwrap();
    println!("Specific time: {}", specific_datetime.format("%Y-%m-%d %H:%M:%S"));

    let mut curr_time = 1742576400;
    while curr_time >= 1742403600 {
        match try_time(curr_time) {
            Ok(string) => {
                println!("{curr_time}: {string}");
            },
            Err(_) => {
                print!("\r{:.2}% done",((1742576400 - curr_time)*100) as f64 / (1742576400 - 1742403600) as f64);
                io::stdout().flush().unwrap();
            }
        }
        curr_time -= 1;
    }
}


fn fun(uVar7: u32) -> u32{
    let uVar7 = uVar7 >> 0xb ^ uVar7;
    let uVar7 = uVar7 ^ (uVar7 & 0x13a58ad) << 7;
    let uVar7 = uVar7 ^ (uVar7 & 0x1df8c) << 0xf;
    let uVar7 = uVar7 ^ uVar7 >> 0x12;
    uVar7
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use super::*;

    #[test]
    fn fun_invertible() {
        let mut total : HashSet<u32> = HashSet::new();
        let mut count = 1;
        for i in 0..=0xFFFFFFFF {
            print!("\r{:.2}% done",(i as u64*100) as f64 / 0x100000000u64 as f64);
            io::stdout().flush().unwrap();
            total.insert(fun(i));
            assert_eq!(total.len(), count);
            count +=1;
        }
    }
}