from pymongo import MongoClient
import urllib.parse

class Mongo_Initiate:

    def __init__(self, db_name) -> None:
        
        self.db_name = db_name
    
    def make_cluster_link(self):
        """Function uses the urllib library to parse the mongo login string and return the ready link"""
        url = 'mongodb://localhost:27017/?'
        params = {
            'readPreference': 'primary',
            'appname': 'MongoDB20Compass',
            'ssl': 'false'
        }
        
        link = url + urllib.parse.urlencode(params)
        
        return link     

    def initiate_mongo(self):
        """
        Function initiates the Mongo Client using the parsed link from the make_cluster_link() function\n
        """
        client = MongoClient(self.make_cluster_link())

        return client

    def make_db_only(self):
        """
        Function creates the new database in Mongo without a column.\n
        Function takes 1 argument: 
            db_content = This is the content of the collections, which need to be in JSON format.
                NOTE: Best way to do it is to pass a list of dictionaries.
        """

        self.initiate_mongo()[f'{self.db_name}']
        
    def create_db_columns(self, column_name, db_content, is_stream=None):
        """
        Function is used to create columns for a database.\n
        Function takes 3 arguments: 
            column_name = The name of the column that is to be created.
            db_content = This is the content of the collections, which need to be in JSON format.
                NOTE: Best way to do it is to pass a list of dictionaries.
            is_stream = This is True when the incomming data should be appended to the db using the insert_many() function. 
            Otherwise, when it's set to False, we will use the insert_one() functionality.
        """

        client = MongoClient(self.make_cluster_link())
        db = client[self.db_name]
        collection = db[column_name]

        if is_stream:
            new_test_db = db_content
            result = collection.insert_many(new_test_db)
        else:
            for i in db_content:
                result = collection.insert_one(i)

        return result

    def make_db_with_column(self, db_content, column_name, is_stream=True):
        """
        Function creates the new database in Mongo with a column.\n
        Function takes 3 arguments: 
            column_name = The name of the column that is to be created.
            db_content = This is the content of the collections, which need to be in JSON format.
                NOTE: Best way to do it is to pass a list of dictionaries.
            is_stream = This is True when the incomming data should be appended to the db using the insert_many() function. 
            Otherwise, when it's set to False, we will use the insert_one() functionality.
        """
        # Creating a new database
        db = self.initiate_mongo()[f'{self.db_name}']
        collection = db[column_name]
        # create a dictionary for the headers for the db
        if is_stream:
            new_test_db = db_content
            result = collection.insert_many(new_test_db)
        else:
            for i in db_content:
                result = collection.insert_one(i)

        return result

    def check_if_databse_exists(self):
        """
        Function is used to check if a database exists or not.\n
        If it exists, function returns True, else False.
        """
        client = MongoClient(self.make_cluster_link())
        db_names = client.list_database_names()
        if self.db_name in db_names:
            return True
        else:
            return False

    def add_multiple_items_to_existing_db(self, column_name, db_content):
        """
        Function is used to add new entries to an existing database.\n
        Function takes 2 arguments:
            column_name = The name of the column that is to be created.\n
            db_content = This is the content of the collections, which need to be a list of dictionaries.
        """
        client = MongoClient(self.make_cluster_link())
        db_to_search = client[self.db_name]
        col_to_search = db_to_search[column_name]

        if len(db_content) > 0:
            col_to_search.insert_many(db_content, ordered=False)
        else:
            pass

    def find_item_in_db(self, column_name, entry_name):
        """
        Function can find specific items in the the MongoDB Collection using the column name as a parameter.\n
        Function takes 2 arguments: 
            column_name = This is the name of the column in mongo.\n
            entry_name = This is the name of the entry that is to be located.
        """
        client = MongoClient(self.make_cluster_link())
        db_to_search = client[self.db_name]
        col_to_search = db_to_search[column_name]

        mongo_list = []
        for i in col_to_search.find({}, {"_id", f"{entry_name}"}):
            if i is not None: 
                mongo_list.append(i)

        return mongo_list
        
    def find_all_items_in_db(self, column_name):
        """
        This function finds all items in the database.\n
        Function takes 1 argument: 
            column_name = This is the name of the column in mongo.
        """
        client = MongoClient(self.make_cluster_link())
        db_to_search = client[self.db_name]
        col_to_search = db_to_search[column_name]
        items_details = col_to_search.find()

        mongo_list = []

        for i in items_details:
            mongo_list.append(i)

        return mongo_list

    def update_specific_item_in_db(self, column_name, col_key=None, old_col_value=None, new_col_values=None):
        """
        This function finds a specific column key:value pair and replaces the value with a new one, removing the old value!\n
        This function takes 5 arguments:
            column_name = This is the name of the column in mongo.\n
            old_col_key = The name of the old column\n
            old_col_value = The value of the column that needs to be changed\n
            new_col_key = The name of the new column\n
            new_col_values = The new value of the column\n
        """
        client = MongoClient(self.make_cluster_link())
        db_to_search = client[self.db_name]
        col_to_search = db_to_search[column_name]

        my_query = { col_key: old_col_value }
        new_values = { "$set": { col_key: new_col_values } }

        col_to_search.update_one(my_query, new_values)

    def update_specific_items_in_db_add_them_to_array(self, column_name, col_key=None, old_col_value=None, new_col_values=None, is_list=None, list_=None):
        """
        This function finds a specific column by it's key and adds the value to an array.\n
        Function is specifically designed for columns that have array values.\n
        If the value is already in the array it will be skipped.\n
        This function takes 5 arguments:
            column_name = This is the name of the column in mongo.\n 
            old_col_key = The name of the old column.\n
            old_col_value = The value of the column that needs to be changed.\n
            new_col_key = The name of the new column.\n
            new_col_values = The new value of the column.\n
            is_list = If this is True, then the function will execute functionality to append array items to db. If False, it will execute the standard workflow.\n
            list_ = The list of items to be appended to db array.
        """

        client = MongoClient(self.make_cluster_link())
        db_to_search = client[self.db_name]
        col_to_search = db_to_search[column_name]

        if is_list == True: 
            my_query = { col_key: old_col_value }
            new_values = { "$addToSet": { col_key: {"$each": [i for i in list_]} } }
            col_to_search.update_one(my_query, new_values)
        else:
            my_query = { col_key: old_col_value }
            new_values = { "$addToSet": { col_key: new_col_values } }

            col_to_search.update_one(my_query, new_values)

    def update_many_items_in_db(self, column_name, entry_to_change, old_value, new_value):
        """
        Function is used to update a single value in many documents using the document id's for iteration.\n
        Function takes 4 arguements:    
            column_name = This is the name of the column in mongo.\n
            iterable = This is a list of all of the id's aquired from the database.\n
            entry_to_change = This is the name of the key whose value we need to change.\n
            new_value = This is the new value. 
        """

        client = MongoClient(self.make_cluster_link())
        db_to_search = client[self.db_name]
        col_to_search = db_to_search[column_name]
        
        col_to_search.update_many({entry_to_change: old_value}, {"$set": { entry_to_change: new_value}})

    def exclude_specific_item_from_db_search(self, column_name, needed_col_name):
        """
        This function finds a specific column key and only displays it, not the rest of the column data.\n
        This function takes 2 arguments:
            column_name = This is the name of the column in mongo.\n
            needed_col_name = This is the name of the specific column that is to be queried. 
        
        """
        client = MongoClient(self.make_cluster_link())
        db_to_search = client[self.db_name]
        col_to_search = db_to_search[column_name]
        items_details = col_to_search.find({}, {f'{needed_col_name}': 0})

        for i in items_details:
            print(i)

    def remove_specific_item_from_db(self, column_name, needed_col_name):
        """
        This function finds a specific column key and removes it from the collection/\n
        This function takes 2 arguments:
            column_name = This is the name of the column in mongo.\n
            needed_col_name = This is the name of the specific column that is to be queried. 
        """
        client = MongoClient(self.make_cluster_link())
        db_to_search = client[self.db_name]
        col_to_search = db_to_search[column_name]

        col_to_search.update_one({}, {'$unset': {f'{needed_col_name}':1}})

    def delete_mongo_db(self):
        """
        Delete a mongo database.
        """
        client = MongoClient(self.make_cluster_link())
        client.drop_database(self.db_name)

#db_ = Mongo_Initiate()
#db_.make_db(name_of_db='test_algo_bot', name_of_column='kline_data', db_content=shit_json, is_stream=False) # uncomment this to create the new database and collection
#db_.find_item_in_db(name_of_db='new_test_db', name_of_column='name_of_column') # uncomment this to search for the keys of a collection
#db_.find_all_items_in_db(name_of_db='new_test_db', name_of_column='name_of_column') # uncomment this to search for all the data in a collection
#db_.find_specific_item_in_db(name_of_db='new_test_db', name_of_column='name_of_column', needed_col_name='Ancient Creatures') # uncomment this to search for a specific item in a collection
#db_.exclude_specific_item_from_db_search(name_of_db='new_test_db', name_of_column='name_of_column', needed_col_name='Ancient Creatures') # uncomment this to exclude a specific item from the search and show everything else
#db_.remove_specific_item_from_db(name_of_db='new_test_db', name_of_column='name_of_column', needed_col_name='Ancient Creatures') # uncomment this to delete a specific item from the column
# db_.update_specific_item_in_db(
#     name_of_db='new_test_db', 
#     name_of_column='name_of_column',
#     old_col_key='Predators',
#     old_col_value='Tiger',
#     new_col_key='Predators',
#     new_col_values='Tiger2, Lion2, Bear2, Shark2, Alligator2'
#     ) 
# uncomment this to replace a specific column values in a column's value
#db_.delete_mongo_db(name_of_db='test_algo_bot')

