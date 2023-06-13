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


// #[tokio::main]
// pub async fn create_get_request() -> Result<(), Box<dyn std::error::Error>> {
//     let response = reqwest::get("http://192.168.1.242:80/api/users").await?.text().await?;

//     if let Ok(json_response) = serde_json::from_str::<serde_json::Value>(&response) {
//         if let serde_json::Value::Object(obj) = json_response {
//             let hashmap: std::collections::HashMap<String, String> = obj
//                 .iter()
//                 .filter_map(|(k, v)| {
//                     if let serde_json::Value::String(s) = v {
//                         Some((k.clone(), s.clone()))
//                     } else {
//                         Some((k.clone(), v.to_string()))
//                     }
//                 })
//                 .collect();
            
//             // Print the hashmap
//             for (key, value) in &hashmap {
//                 println!("Key: {}, Value: {}", key, value);
//             }
//         } else {
//             println!("The JSON response is not an object.");
//         }
//     } else {
//         println!("Failed to parse JSON response.");

//         // Process the response as a string
//         let hashmap: std::collections::HashMap<String, String> = vec![("response".to_owned(), response)].into_iter().collect();
        
//         // Print the hashmap
//         for (key, value) in &hashmap {
//             println!("Key: {}, Value: {}", key, value);
//         }
//     }

//     Ok(())
// }


#[tokio::main]
pub async fn create_get_request() -> Result<(), Box<dyn std::error::Error>> {
    let response = reqwest::get("http://192.168.1.242:80/api/users").await?.text().await?;

    let hashmap: std::collections::HashMap<String, String> = vec![("response".to_owned(), response)].into_iter().collect();
        
    // Print the hashmap
    for (key, value) in &hashmap {
        println!("Key: {}, Value: {}", key, value);
    }

    Ok(())
}
