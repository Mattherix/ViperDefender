import os
import argparse

from sys import exit

from verification import Verification

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

if args.topic_endpoint == None:
    # TODO: Check endpoint
    print("The topic endpoint is not valid")
    exit()

if args.topic_key == None:
    # TODO: Check topic key
    print("The topic endpoint key is not valid")
    exit()

# TODO : Check if the id is valid

verification = Verification(args.path, args.id, args.topic_key, args.topic_endpoint)

