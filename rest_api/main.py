from flask import Flask, jsonify, make_response, render_template, request
from flask_mongoengine import MongoEngine
from datetime import datetime


MONGO_PATH = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
MONGO_DB = "new_test_api_db"
MONGO_COLUMN = "api_db"

app = Flask(__name__)
dat_ = {
    'year': f"{datetime.now().year}",
}

db_name = "Test_API"
DB_URI = MONGO_PATH.format(db_name)
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine(app)
# db.init_app(app)


class User(db.Document): 
    user_id = db.IntField()
    name = db.StringField()
    email = db.StringField()

    def data_to_json(self):
        """converts document data to json format"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }

@app.route('/api/db_populate', methods=['POST'])
def db_populate():
    """
    For this to work, you need to push a post request to URL:
    http://192.168.1.242:80/api/db_populate
    This is best done in Postman
    """
    user_1 = User(user_id = 1, name = "Mustaka", email = "kluna@hui.com")
    user_2 = User(user_id = 2, name = "Manuil", email = "Manuil@hui.com")
    user_3 = User(user_id = 3, name = "Tetko", email = "tetko@hui.com")
    user_4 = User(user_id = 4, name = "Kolzo", email = "kozlo@hui.com")
    
    user_1.save()
    user_2.save()
    user_3.save()
    user_4.save()
    
    return make_response('', 201)


@app.route('/api/users', methods=['GET', 'POST'])
def api_users():
    if request.method == "GET":
        #print(request.method)
        users = []
        for user in User.objects:
            users.append(user)
        return make_response(jsonify(users), 200)
        # The above get's us everything currently in the DB
    elif request.method == "POST":
        user = User(user_id = request.args['user_id'], name = request.args['name'], email = request.args['email'])
        user.save()
        return make_response("", 201)
        # The above updates the database entries. 
        # For this to work you need to do the following in Postman: 


@app.route('/api/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_book(user_id):
#    Here we need to input http://192.168.1.242:80/api/users/2  - 2 is the id of the user, you can choose whichever you need
    if request.method == "GET":
        usr_obj = User.objects(user_id=user_id).first()
        if usr_obj:
            return make_response(jsonify(usr_obj.data_to_json()), 200)
        else:
            return make_response('', 400)
# Here we need to input http://192.168.1.242:80/api/users/2?name=Monovejdil&email=monovejdil@hui.com  - 2 is the id of the user, you can choose whichever you need 
# and then pass the new name and new email in Postman 
    elif request.method == "PUT":
        usr_obj = User.objects(user_id=user_id).first()
        usr_obj.update(name = request.args['name'], email = request.args['email'])
        return make_response('', 204)
# Here we need  http://192.168.1.242:80/api/users/2 and nothing more. Just the request type needs to be Delete in Postman      
    elif request.method == "DELETE":
        usr_obj = User.objects(user_id=user_id).first()
        usr_obj.delete()
        return make_response('', 204)

@app.route('/')
def home():
    return render_template('index.html', data=dat_)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)



"""
There is another way to make the POST, GET, PUT and DELETE API calls. If using Windows like me,
you need to have GitBash installed. Then you need to install the following package: 
pip install --upgrade httpie
Once thats done, you can execute commands from there to make the API call: 

For example to populate the DB: 

http POST http://192.168.1.242:80/api/db_populate


For the more complex requests where you input some additional data: 

echo '{"user_id": "5", "name": "Mario Ciganina", "email":, "m_c@hui.com"}' | http POST http://192.168.1.242:80/api/users 

the above command will add a new user to the DB
"""