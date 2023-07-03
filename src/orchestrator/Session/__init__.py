import os
from pymongo import MongoClient 
import azure.functions as func
import json

from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def main(req: func.HttpRequest) -> func.HttpResponse:
    uri = os.environ["MONGO_URI"]

    client = MongoClient(uri)



    # Create database called TestFilesDB if it doesn't exist 

    db = client["TestFilesDB"]



    # if the request is a GET request, return the request with the good id
    if req.method == "GET":
        id = req.params.get("id")
        if id:
            print(id)
            objInstance = ObjectId(id)
            session = db.sessions.find_one({"_id": objInstance} )
            print("session",session)
            if session:
                return func.HttpResponse(
                    body=JSONEncoder().encode(session),
                    status_code=200
                )
            else:
                return func.HttpResponse(
                    body="Session not found",
                    status_code=404
                )
        else:
            return func.HttpResponse(
                body="Please provide an id",
                status_code=400
            )
    
    # if the request is a POST request, create a new session
    elif req.method == "POST":
        session = {
            "session_ended" : False,
            "session_result": None,
        }
        result = db.sessions.insert_one(session)
        # transform the result to a string
        objInstance = ObjectId(result.inserted_id)
        result = db.sessions.find_one({"_id": objInstance} )
        return func.HttpResponse(
            body= JSONEncoder().encode(result),
            status_code=201
        )
    
    elif req.method == "PATCH": 
        id = req.params.get("id")
        id = ObjectId(id)
        if id:
            session = db.sessions.find_one({"_id": id})
            if session:
                session = req.get_json()
                db.sessions.update_one({"_id": id}, {"$set": session})
                return func.HttpResponse(
                    body="Session updated",
                    status_code=200
                )
            else:
                return func.HttpResponse(
                    body="Session not found",
                    status_code=404
                )
    else :
        return func.HttpResponse(
            body="Method not allowed",
            status_code=405
        )
