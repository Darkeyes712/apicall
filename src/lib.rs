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

pub fn parse_json_data(json_data: &str) -> Result<(), serde_json::Error> {

    let kurec: Value = serde_json::from_str(json_data)?;
    // println!("{}", kurec);
    let nadurven_kurec = kurec.as_array(); // tva go pravi na array
    let index_ = 18;
    if let Some(arr) = nadurven_kurec {
        if let Some(first_obj) = arr.get(index_) {
            if let Some(id) = first_obj.get("_id") {
                println!("ID: {:?}", id);
            }
            if let Some(name) = first_obj.get("name") {
                println!("Name: {:?}", name);
            }
            if let Some(email) = first_obj.get("email") {
                println!("Email: {:?}", email);
            }
        } else {
            println!("Nema takuv index {}, da te eba u glupaka", index_)
        }
    }

    Ok(())
}

#[tokio::main]
pub async fn create_get_request() -> Result<(), Box<dyn std::error::Error>> {
    let response = reqwest::get("http://192.168.1.242:80/api/users").await?.text().await?;
    let hashmap: std::collections::HashMap<String, String> = vec![("response".to_owned(), response)].into_iter().collect();
    
    // for (key, value) in &hashmap {
    //     println!("Key: {}, Value: {}", key, value);
    // } ---> to print the key value data of the hashmap. 

    // Extract the JSON string from the hashmap value
    if let Some(json_data) = hashmap.get("response") {
        // Call the parse_json_data function to parse and process the JSON data
        parse_json_data(json_data)?;
    } else {
        println!("Response not found in the hashmap.");
    }


    Ok(())
}
