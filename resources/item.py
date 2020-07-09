from models.item import ItemModel
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from resources.store import StoreList


class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True)
    parser.add_argument('store_id', type=int, required=True)

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item "{}" not found'.format(name)}

    @jwt_required
    def post(self, name):
        data = Items.parser.parse_args()
        if ItemModel.find_by_name(name):
            return {'message': 'item "{}" already exists'.format(name)}
        item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()
    
    @jwt_required
    def put(self, name):
        data = Items.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()

    @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        item.delete_from_db()
        return {'message': 'item "{}" deleted'.format(name)}


class ItemList(Resource):
    @jwt_required
    def get(self):
        return {'items':[x.json() for x in ItemModel.query.all()]}