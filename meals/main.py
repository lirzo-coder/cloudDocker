from flask import Flask, request, jsonify, make_response
import requests
import json
from flask_restful import Resource, Api
import pymongo
myclient = pymongo.MongoClient("mongodb://mongo:27017/")
app = Flask(__name__)  # initialize Flask
api = Api(app)
mydb = myclient["mydatabase"]
mydishes = mydb["dishes"]
mymeals = mydb["meals"]
mycounters = mydb["counters"] #a collection for counters ID
if mycounters.find_one({"counter": "dishescounter"}) is None: # first time starting up this service as no document with _id ==0 exists
    mycounters.insert_one({"counter": "dishescounter", "count": 0})
    # insert a document into the database to have one "_id" index that starts at 0 and a field named "cur_key"
if mycounters.find_one({"counter": "mealscounter"}) is None: # first time starting up this service as no document with _id ==0 exists
    mycounters.insert_one({"counter": "mealscounter", "count": 0})

class Key(Resource):#dishes by id
    def get(self,key):
        document =mydishes.find_one({"ID": key})
        if document is not None:
            document["_id"] = str(document["_id"])
            document["ID"] = str(document["ID"])
        # Exclude _id attribute from the JSON response
            del document["_id"]
            return make_response(jsonify(document), 200)
        else:
            return make_response(jsonify(-5),404)
    def delete (self,key):
        dish = mydishes.find_one({"ID": key})
        if dish is not None:
            dish_id =str(dish["ID"])
            documents = mymeals.find()
            appetizerneedupdate = False
            mainneedupdate =False
            dessertneedupdate =False
            for document in documents:
                if str(document["appetizer"]) == dish_id:
                    document["appetizer"] = None
                    appetizerneedupdate = True
                if str(document["main"]) == dish_id:
                    document["main"] = None
                    mainneedupdate = True
                if str(document["dessert"]) == dish_id:
                    document["dessert"] = None
                    dessertneedupdate = True
                sumCal =(float)(mymeals.find_one({"ID" :document["ID"]}).get("cal"))
                sumSodium =(float)(mymeals.find_one({"ID" :document["ID"]}).get("sodium"))
                sumSugar =(float)(mymeals.find_one({"ID" :document["ID"]}).get("sugar"))
                if appetizerneedupdate == True:
                    sumCal-=(float)(mydishes.find_one({"ID":dish["ID"]}).get("cal"))
                    sumSodium -=(float)(mydishes.find_one({"ID":dish["ID"]}).get("sodium"))
                    sumSugar -=  (float)(mydishes.find_one({"ID":dish["ID"]}).get("sugar"))
                    mymeals.update_one({"ID": document["ID"]}, {"$set": {"cal": sumCal,"sodium": sumSodium, "sugar":sumSugar,"appetizer":None}})
                if mainneedupdate == True:
                    sumCal-=(float)(mydishes.find_one({"ID":dish["ID"]}).get("cal"))
                    sumSodium -=(float)(mydishes.find_one({"ID":dish["ID"]}).get("sodium"))
                    sumSugar -=  (float)(mydishes.find_one({"ID":dish["ID"]}).get("sugar"))
                    mymeals.update_one({"ID": document["ID"]}, {"$set": {"cal": sumCal,"sodium": sumSodium, "sugar":sumSugar,"main":None}})
                if dessertneedupdate == True:
                    sumCal-=(float)(mydishes.find_one({"ID":dish["ID"]}).get("cal"))
                    sumSodium -=(float)(mydishes.find_one({"ID":dish["ID"]}).get("sodium"))
                    sumSugar -=  (float)(mydishes.find_one({"ID":dish["ID"]}).get("sugar"))
                    mymeals.update_one({"ID": document["ID"]}, {"$set": {"cal": sumCal,"sodium": sumSodium, "sugar":sumSugar,"dessert":None}})
            mydishes.delete_one({"ID": key})
            return make_response(jsonify(dish_id), 200)
        return make_response(jsonify(-5), 404)

class Name(Resource):#dishes by name 
    def get(self, key_name):
        document =mydishes.find_one({"name": key_name})
        if document is not None:
            document["_id"] = str(document["_id"])
            document["ID"] = str(document["ID"])
        # Exclude _id attribute from the JSON response
            del document["_id"]
            return make_response(jsonify(document), 200)
        else:
            return make_response(jsonify(-5),404)

    def delete (self, key_name):
        dish = mydishes.find_one({"name": key_name})
        if dish is not None:
            dish_id =str(dish["ID"])
            documents = mymeals.find()
            appetizerneedupdate = False
            mainneedupdate =False
            dessertneedupdate =False
            for document in documents:
                if str(document["appetizer"]) == dish_id:
                    document["appetizer"] = None
                    appetizerneedupdate = True
                if str(document["main"]) == dish_id:
                    document["main"] = None
                    mainneedupdate = True
                if str(document["dessert"]) == dish_id:
                    document["dessert"] = None
                    dessertneedupdate = True
                sumCal =(float)(mymeals.find_one({"ID" :document["ID"]}).get("cal"))
                sumSodium =(float)(mymeals.find_one({"ID" :document["ID"]}).get("sodium"))
                sumSugar =(float)(mymeals.find_one({"ID" :document["ID"]}).get("sugar"))
                if appetizerneedupdate == True:
                    sumCal-=(float)(mydishes.find_one({"ID":dish["ID"]}).get("cal"))
                    sumSodium -=(float)(mydishes.find_one({"ID":dish["ID"]}).get("sodium"))
                    sumSugar -=  (float)(mydishes.find_one({"ID":dish["ID"]}).get("sugar"))
                    mymeals.update_one({"ID": document["ID"]}, {"$set": {"cal": sumCal,"sodium": sumSodium, "sugar":sumSugar,"appetizer":None}})
                if mainneedupdate == True:
                    sumCal-=(float)(mydishes.find_one({"ID":dish["ID"]}).get("cal"))
                    sumSodium -=(float)(mydishes.find_one({"ID":dish["ID"]}).get("sodium"))
                    sumSugar -=  (float)(mydishes.find_one({"ID":dish["ID"]}).get("sugar"))
                    mymeals.update_one({"ID": document["ID"]}, {"$set": {"cal": sumCal,"sodium": sumSodium, "sugar":sumSugar,"main":None}})
                if dessertneedupdate == True:
                    sumCal-=(float)(mydishes.find_one({"ID":dish["ID"]}).get("cal"))
                    sumSodium -=(float)(mydishes.find_one({"ID":dish["ID"]}).get("sodium"))
                    sumSugar -=  (float)(mydishes.find_one({"ID":dish["ID"]}).get("sugar"))
                    mymeals.update_one({"ID": document["ID"]}, {"$set": {"cal": sumCal,"sodium": sumSodium, "sugar":sumSugar,"dessert":None}})
            mydishes.delete_one({"name": key_name})
            return make_response(jsonify(dish_id), 200)
        return make_response(jsonify(-5), 404)


class meal_name(Resource):
    def get(self, m_name):
       document =mymeals.find_one({"name": m_name})
       if document is not None:
            document["_id"] = str(document["_id"])
            document["ID"] = str(document["ID"])
            if document["appetizer"] is not  None:
                document["appetizer"] = str(document["appetizer"])
            if document["main"] is not None:
                document["main"] = str(document["main"])
            if document["dessert"] is not None:
                document["dessert"] = str(document["dessert"])
        # Exclude _id attribute from the JSON response
            del document["_id"]
            return make_response(jsonify(document), 200)
       else:
            return make_response(jsonify(-5),404)

    def delete (self, m_name):
        meal = mymeals.find_one({"name": m_name})
        if meal is not None:
        # Get the ID of the dish
            meal_id =str(meal["ID"])
        # Delete the dish
            mymeals.delete_one({"name": m_name})
            return make_response(jsonify(meal_id), 200)
        return make_response(jsonify(-5), 404)

class meal_id(Resource):
    def get(self, id):
        document =mymeals.find_one({"ID": id})
        if document is not None:
            document["_id"] = str(document["_id"])
            document["ID"] = str(document["ID"])
            if document["appetizer"] is not  None:
                document["appetizer"] = str(document["appetizer"])
            if document["main"] is not None:
                document["main"] = str(document["main"])
            if document["dessert"] is not None:
                document["dessert"] = str(document["dessert"])
        # Exclude _id attribute from the JSON response
            del document["_id"]
            return make_response(jsonify(document), 200)
        else:
            return make_response(jsonify(-5),404)
    def delete (self,id):
        meal = mymeals.find_one({"ID": id})
        if meal is not None:
        # Get the ID of the dish
            meal_id =str(meal["ID"])
        # Delete the dish
            mymeals.delete_one({"ID": id})
            return make_response(jsonify(meal_id), 200)
        return make_response(jsonify(-5), 404)

class dishes(Resource):
    def get(self):
        projection = {"_id": 0}
        collection_data = list(mydishes.find({},projection))
        collection_length = len(collection_data)
        if collection_length > 0:
            for document in collection_data:
                document["ID"] = str(document["ID"])
            return make_response(jsonify(collection_data), 200)
        else:
            return make_response(jsonify(),200)
        
    def delete(self):
        global dishC
        response = -1
        return make_response(jsonify(response), 400)

    def post(self):
         #check if it is a application/json if not return 0 and 415 error code
        if request.content_type != "application/json" or request.args:
            return make_response(jsonify(0), 415)
        dish_data = request.get_json()
        temp_dish = request.args.get('name')
        if 'name' not in dish_data or temp_dish is not None or request.get_json()['name'] =='':#check the attribute name and if its empty- not correct return -1 and 400
            return make_response(jsonify(-1),400)

        dish_name = dish_data['name'] #get dish name
        duplicate_dish = mydishes.find_one({"name": dish_name})
        if duplicate_dish is not None:
            return make_response(jsonify(-2), 400)
        query = dish_name
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url,headers={'X-Api-Key': '5Vocvb2jhJTzHS2WVPNUeg==na0EAyw5FC9Tc7Us'})
        if response.status_code == requests.codes.ok and len(response.json()) > 0:
            info = list(response.json())
            cal = 0
            size = 0
            sodium = 0
            sugar = 0
            counter = 0
            for temp_dish in info:
                cal += (float)(temp_dish['calories'])
                size += (float)(temp_dish['serving_size_g'])
                sodium += (float)(temp_dish['sodium_mg'])
                sugar += (float)(temp_dish['sugar_g'])
            dishc = mycounters.find_one({"counter":"dishescounter"})
            dishID = dishc["count"]
            dishID += 1
            mycounters.update_one({"counter": "dishescounter"}, {"$set": {"count": dishID}})
            arr = {'name': dish_name,"ID": dishID, 'cal': cal, 'size': size, 'sodium': sodium,
                             'sugar': sugar}
            mydishes.insert_one(arr)
            response =str(dishID)
            return make_response(jsonify(response), 201) #means succesfully added
        elif response.status_code != requests.codes.ok: #internal problem in server
            response = -4
            return make_response(jsonify(response), 400)
        else:# means empty response - dish doesnt exsists.
            response = -3
            return make_response(jsonify(response), 400)

class meals(Resource):
    def delete(self):
        response = -1
        return make_response(jsonify(response), 400)

    def get(self):
        if len(request.args) == 0:#means regular get 
            projection = {"_id": 0}
            collection_data = list(mymeals.find({},projection))
            collection_length = len(collection_data)
            if collection_length > 0:
                for document in collection_data:
                    document["ID"] = str(document["ID"])
                    if document["appetizer"] is not  None:
                        document["appetizer"] = str(document["appetizer"])
                    if document["main"] is not None:
                        document["main"] = str(document["main"])
                    if document["dessert"] is not None:
                        document["dessert"] = str(document["dessert"])
                return make_response(jsonify(collection_data), 200)   
            else:
                return make_response(jsonify(),200)
        else:
            diet_name = request.args.get('diet')
            if diet_name is not None:
                url = f"http://diets-service:{80}/diets/"+diet_name
                response = requests.get(url)
                diet_data = response.json()
                diet_cal = diet_data['cal']
                diet_sodium = diet_data['sodium']
                diet_sugar = diet_data['sugar']
                query = {
                'cal': {'$lte': diet_cal},
                'sodium': {'$lte': diet_sodium},
                'sugar': {'$lte': diet_sugar}
                }
                diets_meals =list(mymeals.find(query))
                collection_length = len(diets_meals)
                if collection_length > 0: #found items with those values
                    for document in diets_meals:
                        document["ID"] = str(document["ID"])
                        del document["_id"]
                        document["appetizer"] = str(document["appetizer"])
                        document["main"] = str(document["main"])
                        document["dessert"] = str(document["dessert"])
                    return make_response(jsonify(diets_meals), 200) 
                else:
                    response = "Diet {} not found".format(diet_name)
                    return make_response(jsonify(response),404)
                

    def post (self):
        if request.content_type != "application/json" or request.args:
            return make_response(jsonify(0), 415)
        data = request.get_json()
        if(('name' not in data) or ('appetizer' not in data) or ('main' not in data) or ('dessert' not in data)
                or request.get_json()['name'] =='' or request.get_json()['main'] =='' or  request.get_json()['dessert'] ==''or request.get_json()['appetizer'] ==''):
            return make_response(jsonify(-1), 400)
        if request.args:
            response = 0
            return make_response(jsonify(response), 415)
        meal_data = request.get_json()
        meal_name = meal_data['name']
        duplicate_meal = mymeals.find_one({"name": meal_name})
        if duplicate_meal is not None:
            return make_response(jsonify(-2), 400)
        meal_appetizer_id = (int)(meal_data['appetizer'])
        meal_main_id =(int)(meal_data['main'])
        meal_dessert_id = (int)(meal_data['dessert'])
        appetizer_found = False
        main_found = False
        dessert_found = False
        appEx = mydishes.find_one({"ID":meal_appetizer_id})
        if appEx is not None:
                appetizer_found = True
        mainEx = mydishes.find_one({"ID":meal_main_id})
        if mainEx is not None:     
                main_found = True
        dessertEx = mydishes.find_one({"ID":meal_dessert_id})
        if dessertEx is not None:
                dessert_found = True
        if appetizer_found and main_found and dessert_found :
            mealc = mycounters.find_one({"counter":"mealscounter"})
            mealID = mealc["count"]
            mealID += 1
            mycounters.update_one({"counter": "mealscounter"}, {"$set": {"count": mealID}})
            sumCal = (float)(mydishes.find_one({"ID": meal_appetizer_id}).get("cal")) + (float)(mydishes.find_one({"ID": meal_main_id}).get("cal")) + (float)(mydishes.find_one({"ID": meal_dessert_id}).get("cal"))
            sumSodium =(float)(mydishes.find_one({"ID": meal_appetizer_id}).get("sodium")) +(float)(mydishes.find_one({"ID": meal_main_id}).get("sodium")) +(float)(mydishes.find_one({"ID": meal_dessert_id}).get("sodium"))
            sumSugar = (float)(mydishes.find_one({"ID": meal_appetizer_id}).get("sugar")) + (float)(mydishes.find_one({"ID": meal_main_id}).get("sugar")) +  (float)(mydishes.find_one({"ID": meal_dessert_id}).get("sugar"))
            meal = {'name':meal_name, 'ID':mealID,'appetizer': meal_appetizer_id, 'main':meal_main_id,'dessert':meal_dessert_id,'cal':sumCal,'sodium':sumSodium,
                             'sugar':sumSugar}
            mymeals.insert_one(meal)
            response =str(mealID)
            return make_response(jsonify(response), 201)
        else:
            response = -5
            return make_response(jsonify(response), 400)
class changes(Resource):
    def put(self,meal_id):
        if request.content_type != "application/json":
            return make_response(jsonify(0), 415)
        meal_data = request.get_json()
        if (('name' not in meal_data) or ('appetizer' not in meal_data) or ('main' not in meal_data) or (
                'dessert' not in meal_data)
                or request.get_json()['name'] == '' or request.get_json()['main'] == '' or request.get_json()[
                    'dessert'] == '' or request.get_json()['appetizer'] == ''):
            return make_response(jsonify(-1), 400)
        meal = mymeals.find_one({"ID":meal_id})
        if meal is not None:
            need_update = False
            meal_name = (meal_data['name'])
            meal_appetizer_id = (int)(meal_data['appetizer'])
            meal_main_id = (int)(meal_data['main'])
            meal_dessert_id = (int)(meal_data['dessert'])
            appetizer_found = False
            main_found = False
            dessert_found = False
            meal_appetizer = mydishes.find_one({"ID":meal_appetizer_id})
            if meal_appetizer is not None:
                    appetizer_found = True
            meal_main = mydishes.find_one({"ID":meal_main_id})
            if meal_main is not None:
                    main_found = True
            meal_dessert = mydishes.find_one({"ID":meal_dessert_id})
            if meal_dessert is not None:
                    dessert_found = True
            if appetizer_found and main_found and dessert_found:
                if (mymeals.find_one({"ID": meal_id}).get("name"))  != meal_name:
                    mymeals.update_one({"ID": meal_id}, {"$set": {"name": meal_name}})
                if (mymeals.find_one({"ID": meal_id}).get("appetizer")) != meal_appetizer_id:
                    mymeals.update_one({"ID": meal_id}, {"$set": {"appetizer": meal_appetizer_id}})
                    need_update = True
                if (mymeals.find_one({"ID": meal_id}).get("main")) != meal_main_id:
                    mymeals.update_one({"ID": meal_id}, {"$set": {"main": meal_main_id}})
                    need_update = True
                if (mymeals.find_one({"ID": meal_id}).get("dessert")) != meal_dessert_id:
                    mymeals.update_one({"ID": meal_id}, {"$set": {"dessert": meal_dessert_id}})
                    need_update = True
                if need_update == True:
                    sumCal = (float)(mydishes.find_one({"ID": meal_appetizer_id}).get("cal")) + (float)(mydishes.find_one({"ID": meal_main_id}).get("cal")) + (float)(mydishes.find_one({"ID": meal_dessert_id}).get("cal"))
                    sumSodium =(float)(mydishes.find_one({"ID": meal_appetizer_id}).get("sodium")) +(float)(mydishes.find_one({"ID": meal_main_id}).get("sodium")) +(float)(mydishes.find_one({"ID": meal_dessert_id}).get("sodium"))
                    sumSugar = (float)(mydishes.find_one({"ID": meal_appetizer_id}).get("sugar")) + (float)(mydishes.find_one({"ID": meal_main_id}).get("sugar")) +  (float)(mydishes.find_one({"ID": meal_dessert_id}).get("sugar"))
                    mymeals.update_one({"ID": meal_id}, {"$set": {"cal": sumCal}})
                    mymeals.update_one({"ID": meal_id}, {"$set": {"sodium": sumSodium}})
                    mymeals.update_one({"ID": meal_id}, {"$set": {"sugar": sumSugar}})
                response = str(meal_id)
                return make_response(jsonify(response), 200)
            else:
                return make_response(jsonify(-5), 400)
        else:
            return make_response(jsonify(-5), 400)


api.add_resource(changes, '/meals/<int:meal_id>')
api.add_resource(meal_name, '/meals/<string:m_name>')
api.add_resource(meal_id, '/meals/<int:id>')
api.add_resource(meals, '/meals')
api.add_resource(dishes, '/dishes')
api.add_resource(Key, '/dishes/<int:key>')
api.add_resource(Name, '/dishes/<string:key_name>')
if __name__ == '__main__':
    pass
