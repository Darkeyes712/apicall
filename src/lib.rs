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

pub fn get_value_from_option<T>(option: Option<T>) -> Option<T> {
    match option {
        Some(value) => Some(value),
        None => None,
    }
}

pub fn parse_json_data(json_data: &str, index_: usize, key_name: &str) -> Result<(), serde_json::Error> {
    /// Function is used to parse a json file and return an array data type.
    /// Function takes 3 arguments: 
    ///     json_data = This is the json data, which is in a string format.
    ///     index_ = This is an integer of the index you want to query.
    ///     key_name = This is the name of the specific key you want to query.
    let initial_json_value: Value = serde_json::from_str(json_data)?;
    let json_array = initial_json_value.as_array(); // tva go pravi na array
    if let Some(arr) = json_array {
        if let Some(first_obj) = arr.get(index_) { // this gets into the array and the Some() checks if the value exists, if not, it will return Null. 
            println!("{}", first_obj);
            if let Some(key) = first_obj.get(key_name) {
                println!("{:?}", key);
            }
        } else {
            println!("Nema takuv index {}, da te eba u glupaka", index_)
        }
    } else {
        println!("Nema value u toa aray, da te eba u glupaka")
    }

    Ok(())
}

#[tokio::main]
pub async fn create_get_request() -> Result<(), Box<dyn std::error::Error>> {
    let response = reqwest::get("http://192.168.1.242:80/api/users").await?.text().await?;
    let hashmap: std::collections::HashMap<String, String> = vec![("response".to_owned(), response)].into_iter().collect();
    
    // Extract the JSON string from the hashmap value
    if let Some(json_data) = hashmap.get("response") {
        // Call the parse_json_data function to parse and process the JSON data
        parse_json_data(json_data, 1, "_id")?;
    } else {
        println!("Response not found in the hashmap.");
    }

    Ok(())
}
