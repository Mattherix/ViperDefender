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
        hash = req.params.get("hash")
        if hash:
            session = db.files.find_one({"hash": hash} )
            if session:
                return func.HttpResponse(
                    body=JSONEncoder().encode(session),
                    status_code=200
                )
            else:
                return func.HttpResponse(
                    body="Hash not found",
                    status_code=404
                )
        else:
            return func.HttpResponse(
                body="Please provide a hash",   
                status_code=400
            )
    
    # if the request is a POST request, create a new file
    elif req.method == "POST":
        hash = req.params.get("hash")
        # Check if the hash is already in the database
        if db.files.find_one({"hash": hash}):
            return func.HttpResponse(
                body="Hash already in the database",
                status_code=409
            )
        scan_result = req.params.get("result")
        # id is hash
        result = db.files.insert_one({"hash": hash, "session_result": scan_result})
        # transform the result to a string
        objInstance = ObjectId(result.inserted_id)
        result = db.files.find_one({"_id": objInstance} )
        return func.HttpResponse(
            body= JSONEncoder().encode(result),
            status_code=201
        )
    
    else :
        return func.HttpResponse(
            body="Method not allowed",
            status_code=405
        )
