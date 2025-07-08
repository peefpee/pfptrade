from pymongo import MongoClient
import userclass
import tradeclass
class database:
    def __init__ (self, url: str,databasename:str = "database",collectionname:str = "users"):
        self.connectionurl = url
        self.client = MongoClient(self.connectionurl)
        self.databasename = databasename
        self.collectionname = collectionname
    
    def checkuser (self, username: str,email : str = None):
        db = self.client[self.databasename]
        collection = db[self.collectionname]
        user = collection.find_one({"username": username})
        if user:
            u =  True
        else:   
            u= False
        email = collection.find_one({"email": email})
        if email: 
            e = True    
        else:
            e = False
        if u or e:
            return True
        else:
            return False
    def nextid(self):
        db = self.client[self.databasename]
        collection = db[self.collectionname]
        last_user = collection.find_one(sort=[("id", -1)])
        if last_user:
            return last_user["id"] + 1
        else:
            return 1
    def adduser(self, user: userclass.UserClass):
        db = self.client[self.databasename]
        collection = db[self.collectionname]
        user_dict = user.model_dump()
        user_dict["id"] = self.nextid()
        collection.insert_one(user_dict)
        return user_dict["id"]
    def validateuser(self, email: str, password: str):
        db = self.client[self.databasename]
        collection = db[self.collectionname]
        user = collection.find_one({"email": email, "password": password})
        if user:
            return True
        else:
            return False
    def getuserdetails(self, id: int = None, email: str = None, username: str = None):
        db = self.client[self.databasename]
        collection = db[self.collectionname]
        user = None

        if id is not None:
            user = collection.find_one({"id": id})
        elif email is not None:
            user = collection.find_one({"email": email})
        elif username is not None:
            user = collection.find_one({"username": username})
        
        if not user:
            return {"error": "User not found"}
        user = userclass.UserClass(**user)

        return user
    def addorder(self,userid:int,order:tradeclass.order):
        db = self.client[self.databasename]
        collection = db[self.collectionname]
        user = collection.find_one({"id": userid})
        if not user:
            return {"error": "User not found"}
        if "orders" not in user:
            user["orders"] = []
        order_dict = order.model_dump()
        user["orders"].append(order_dict)
        collection.update_one({"id": userid}, {"$set": {"orders": user["orders"]}})
        return order_dict["id"]