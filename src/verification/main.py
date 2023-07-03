import os
import argparse

from sys import exit

from download import download_and_unzip_files
from verification import Verification
from events import Event
from check_id import is_id_valid

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="The path of the executable to test")
parser.add_argument("--id", help="The id of the verification")
parser.add_argument("--topic-endpoint", help="The topic endpoint, used to send the result")
parser.add_argument("--topic-key", help="The topic endpoint key, used to send the result")
parser.add_argument("--fapp-endpoint", help="The function app endpoint key, used to check the id")
args = parser.parse_args()

if args.path == None:
    print("Please specify the path of the executable to test")
    exit()

if not os.path.exists(args.path):
    print("The path of the executable to test is not valid")
    exit()

try:
    event = Event(args.topic_key, args.topic_endpoint)
except:
    print("The topic endpoint or endpoint key is not valid")
    exit()

if args.fapp_endpoint == None:
    print("Please specify the endpoint in order to check the id")
    exit()

# Check if the id is valid
if is_id_valid(path.id):
    print("Please specify a valid id")
    exit()

download_and_unzip_files()
verification = Verification(args.path, args.id, event)

