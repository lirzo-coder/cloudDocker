from flask import Flask, request, jsonify, make_response
import requests
import json
from flask_restful import Resource, Api
import pymongo
app = Flask(__name__)  # initialize Flask
api = Api(app)
myclient = pymongo.MongoClient("mongodb://mongo:27017/")
mydb = myclient["mydatabase"]
mydiets = mydb["diets"]
class diets(Resource):
    def post(self):
         #check if it is a application/json if not return 0 and 415 error code
        if request.content_type != "application/json":
            response ="POST expects content type to be application/json"
            return make_response(jsonify(response), 415)
        diet_data = request.get_json()
        diet_name = diet_data['name']
        duplicate_diet = mydiets.find_one({"name": diet_name})
        if(('name' not in diet_data) or ('cal' not in diet_data) or ('sodium' not in diet_data) or ('sugar' not in diet_data)
                or request.get_json()['name'] =='' or request.get_json()['cal'] =='' or  request.get_json()['sugar'] ==''or request.get_json()['sodium'] ==''):
                response = "Incorrect POST format"
                return make_response(jsonify(response), 422)
        if duplicate_diet is not None:#diet already exits
            response ="Diet with {} already exists".format(diet_name)
            return make_response(jsonify(response), 422)
        
        diet_name = diet_data['name']
        diet_cal =diet_data['cal']
        diet_sodium =diet_data['sodium']
        diet_sugar =diet_data['sugar']
        arr = {'name': diet_name,'cal': diet_cal,'sodium': diet_sodium,
                             'sugar': diet_sugar}
        mydiets.insert_one(arr)
        response="Diet {} was created successfully".format(diet_name)
        return make_response(jsonify(response), 201) #means succesfully added
    def get(self):
        projection = {"_id": 0}
        collection_data = list(mydiets.find({},projection))
        collection_length = len(collection_data)
        if collection_length > 0:
            for document in collection_data:
                return make_response(jsonify(collection_data), 200)
        else:
            return make_response(jsonify(),200)
class Name(Resource):
    def get(self, key_name):
        document =mydiets.find_one({"name": key_name})
        if document is not None:
            document["_id"] = str(document["_id"])
        # Exclude _id attribute from the JSON response
            del document["_id"]
            return make_response(jsonify(document), 200)
        else:
            response="Diet {} not found".format(key_name)
            return make_response(jsonify(response),404)
    

api.add_resource(diets, '/diets')
api.add_resource(Name, '/diets/<string:key_name>')
if __name__ == '__main__':
    pass