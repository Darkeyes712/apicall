use std::io::{self, Write};
use reqwest::Client;
use serde_json::{json, Map, Value, Error};
use serde::de::Error as SerdeError;
use std::collections::HashMap;
use::tokio::main;

#[derive(serde::Serialize)]
struct Post {
    name: String,
    age: u32,
    email: String
}

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

pub fn parse_json_data(json_data: &str) -> Result<Vec<Value>, Error> {
    let initial_json_value: Value = serde_json::from_str(json_data)?;
    let json_array = initial_json_value.as_array().ok_or_else(|| {
        Error::custom("JSON data is not an array")
    })?;

    Ok(json_array.to_owned())
}

#[tokio::main]
pub async fn create_get_request() -> Result<(), Box<dyn std::error::Error>> {
    let index: usize = 0;
    let response = reqwest::get("http://192.168.1.242:80/api/users").await?.text().await?;
    let json_array = parse_json_data(&response).unwrap();
    if let Some(indexed_array) = json_array.get(index) {
        if let Some(id) = indexed_array.get("_id") {
            println!("{:?}", id);
        }
        if let Some(email) = indexed_array.get("email") {
            println!("{:?}", email);
        }
        if let Some(name) = indexed_array.get("name") {
            println!("{:?}", name);
        }
        if let Some(user_id) = indexed_array.get("user_id") {
            println!("{:?}", user_id);
        }
    }

    Ok(())
}

#[tokio::main]
pub async fn create_post_request() -> Result<(), Box<dyn std::error::Error>> {

    let json_person = Post {
        name: String::from("Kolzo"),
        age: 28,
        email: String::from("kolzoe@example.com"),
    };
    let json_string = serde_json::to_string(&json_person).unwrap();
    let client = Client::new();

    let response = client
    .post("https://httpbin.org/post")
    .body(json_string)  // Set the request body
    .send()
    .await?;

    // Handle the response
    if response.status().is_success() {
        let body = response.text().await?;
        let json_object: serde_json::Value = serde_json::from_str(&body)?;

        // Parse the "data" field as a JSON string
        if let Some(data) = json_object.get("data") {
            if let Some(data_string) = data.as_str() {
                let data_json: serde_json::Value = serde_json::from_str(data_string)?;

                // Iterate over the parsed "data" JSON object's contents
                if let Some(data_map) = data_json.as_object() {
                    for (key, value) in data_map {
                        println!("Key: {:?}, Value: {:?}", key, value);
                    }
                }
            }
        }
    } else {
        println!("POST request failed with status: {}", response.status());
    }

Ok(())

}


