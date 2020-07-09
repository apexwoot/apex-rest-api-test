import os
from flask import Flask
from flask_jwt import JWT
from flask_restful import Resource, Api

from resources.item import Items, ItemList
from resources.store import Stores, StoreList
from security import authenticate, identity
from resources.user import UserRegister

app = Flask(__name__)
app.secret_key = 'apex'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_KEY','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
jwt = JWT(app, authenticate, identity)


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Stores, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/')

api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000)