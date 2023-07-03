import os
import argparse

from sys import exit

from download import download_and_unzip_files
from verification import Verification
from events import Event

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="The path of the executable to test")
parser.add_argument("--id", help="The id of the verification")
parser.add_argument("--topic-endpoint", help="The topic endpoint, used to send the result")
parser.add_argument("--topic-key", help="The topic endpoint key, used to send the result")
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

# TODO : Check if the id is valid

download_and_unzip_files()
verification = Verification(args.path, args.id, event)

