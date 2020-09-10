from flask import Flask
from flask import request
from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse


app = Flask(__name__)
api = Api(app)

items = []


class ItemCollection(Resource):
    def get(self):
        if not items:
            return {'Error': 'No one items found in store back'}, 403
        return {'items': items}, 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help='Field title should be str')
    parser.add_argument('amount', type=int, required=True, help='Field amount should be int')
    parser.add_argument('price', type=float, required=True, help='Field price should be float')

    def get(self, _id):
        item = next(filter(lambda x: x['id'] == _id, items), None)
        if not item:
            return {'Error': 'Item with that id not found'}, 404
        return {'item': item}, 200

    def post(self, _id):
        item = next(filter(lambda x: x['id'] == _id, items), None)
        if item:
            return {'Error': 'Item with that id already exists'}, 400
        data = Item.parser.parse_args()
        item = {
            'id': _id,
            'title': data['title'],
            'amount': data['amount'],
            'price': data['price']
        }
        items.append(item)
        return {'Message': 'Item created'}, 201

    def put(self, _id):
        item = next(filter(lambda x: x['id'] == _id, items), None)
        if not item:
            return {'Error': 'Item with that id not found'}, 404
        data = Item.parser.parse_args()
        item.update(data)
        return {'item': item}, 202

    def delete(self, _id):
        global items
        new_items = list(filter(lambda x: x['id'] != _id, items))
        if items == new_items:
            return {'Error': 'Item with that id not found'}, 404
        items = new_items
        return {'Message': 'Item deleted'}, 202


api.add_resource(ItemCollection, '/api/v1/items')
api.add_resource(Item, '/api/v1/item/<int:_id>')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
