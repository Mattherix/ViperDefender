from pymongo import MongoClient
import os

uri = os.environ["MONGO_URI"]

client = MongoClient(uri)



# Create database called TestFilesDB if it doesn't exist 

db = client["TestFilesDB"]



# Create collection called Sessions if it doesn't exist

sessions_collection = db["Sessions"]

# Create a collection called FilesTested if it doesn't exist

files_collection = db["FilesTested"]

print("Database connected successfully")

# Add a document to the Sessions collection


# export the database, collection and document to be used in other files
  
def get_db():
    return db

def get_sessions_collection():
  return sessions_collection

def get_files_tested_collection():
  return files_collection