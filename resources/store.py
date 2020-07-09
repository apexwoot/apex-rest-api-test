from models.store import StoreModel
from app import jwt
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Stores(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'store "{}" not found'.format(name)}

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "store '{}' already exists".format(name)}
        store = StoreModel(name)
        store.save_to_db()
        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        store.delete_from_db()
        return {'message': "item '{}' deleted".format(name)}


class StoreList(Resource):
    def get(self):
        return {'stores':[x.json() for x in StoreModel.query.all()]}