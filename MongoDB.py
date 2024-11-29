from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["host"]
        self.collection = self.db["movies"]
        self.requestsCollection=self.db["requests"]
        self.expensesCollection=self.db["expenses"]
    
    def handle_movie_requests(self,content):
        self.requestsCollection.insert_one({"name":content['name'],"message":content['message'],"status":"Created"})
    
    def construct_main_page(self):
        jsonMerged=[]
        recommended = self.collection.find({"recommended":True,"disabled":{"$ne":True}}).sort({"popularity":-1}).limit(20)      
        # getting Most Popular Films
        mostPopular=self.collection.find({"disabled":{"$ne":True}}).sort({"popularity":-1}).limit(20)
        # Getting Highest Rated Movies
        highestRated=self.collection.find({"disabled":{"$ne":True}}).sort({"vote_average":-1}).limit(50)
        # Grabbing 24 top films 
        for i in recommended:
            if (len(jsonMerged)<15):
                jsonMerged.append(i)
        for i in mostPopular:
            if (len(jsonMerged)<6 and i not in jsonMerged):
                jsonMerged.append(i)
        for i in highestRated:
            if (len(jsonMerged)<24 and i not in jsonMerged):
                jsonMerged.append(i)
        
        return jsonMerged
    
    def movie_search_bar(self,query):
        findQuery={"title":{"$regex" : query,"$options": 'i'},"disabled":{"$ne":True}}
        return(self.collection.find(findQuery,{"video":1,"title":1}).sort({"release_date":1}).limit(20))
    
    def movie_search_screen(self,query):
        findQuery={"title":{"$regex" : query,"$options": 'i'},"disabled":{"$ne":True}}
        result=[]
        values=(self.collection.find(findQuery).sort({"release_date":1}).limit(20))
        for i in values:
            result.append(i)
        return result
    
    # Dashboard Updates
    def getRequests(self):
        return(self.requestsCollection.find({"status":{'$in':["Created","In Progress"]}}).limit(100))

    def updateRequestStatus(self,request):
        try:
            id=(request['_id']['$oid'])
            try:
                item=self.requestsCollection.find_one({"_id":ObjectId(id)})
                if (item['status']=="Created"):
                    self.requestsCollection.find_one_and_update({"_id":ObjectId(id)},{'$set':{'status':'In Progress'}})
                    return {"status":200,"message":"Moved to 'In Progress'"}
                elif (item['status']=="In Progress"):
                    self.requestsCollection.find_one_and_update({"_id":ObjectId(id)},{'$set':{'status':'Completed'}})
                    return {"status":200,"message":"Moved to 'Completed'"}
                elif (item['status']=="Completed"):
                    return {"status":200,"message":"Its already completed tf you want to do with this???'"}
                else:
                    return {"status":500,"message":"Unrecognized Status"}
            except:
                return {"status":404,"message":"Error in handling Request"}
        except:
            return {"status":400,"message":"Failed to parse json token"}