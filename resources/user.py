from models.user import UserModel
from flask_restful import Resource, reqparse

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username']) 
        if user:
            return {'message': 'user "{}" already exists'.format(data['username'])}
        else:
            user = UserModel(**data)
            user.save_to_db()
            return {'message': 'user "{}" cleated'.format(data['username'])}