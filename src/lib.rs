use std::io::{self, Write};
use reqwest;
use serde_json::{json, Map, Value};
use std::collections::HashMap;
use::tokio::main;


pub fn print_to_terminal(prompt:&str) {
    println!("{}", prompt);
    std::io::stdout().flush().unwrap();
}

pub fn get_user_input(user_input:&str) -> String{
    print_to_terminal(user_input);
    let mut usr_inp = String::new();
    let stdin = io::stdin();
    stdin.read_line(&mut usr_inp);
   
    return usr_inp;
}

#[tokio::main]
pub async fn create_get_request() -> Result<(), Box<dyn std::error::Error>> {
    let response = reqwest::get("http://192.168.1.242:80/api/users").await?.text().await?;
    let json_response: serde_json::Value = serde_json::from_str(&response)?;
    
    println!("{}", json_response);

    if let Some(obj) = json_response.as_object() {
        let hashmap: std::collections::HashMap<String, String> = obj
            .iter()
            .filter_map(|(k, v)| {
                if let serde_json::Value::String(s) = v {
                    Some((k.clone(), s.clone()))
                } else {
                    None
                }
            })
            .collect();
        // NOTE: Figure out how to make the hashmap work so that it can be printed. 
        // for (key, value) in hashmap {
        //     println!("Key: {}, Value: {}", key, value);
        // }
        println!("{:?}", hashmap);
    }

    Ok(())
}

// pub fn create_post_request() {
//     println!("POST");
// }

