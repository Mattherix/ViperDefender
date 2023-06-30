import os
import argparse
from verification import Verification



parser = argparse.ArgumentParser()
parser.add_argument("--path", help="The path of the executable to test")
parser.add_argument("--id", help="The id of the verification")
args = parser.parse_args()
if args.path == None:
    print("Please specify the path of the executable to test")
    exit()
if not os.path.exists(args.path):
    print("The path of the executable to test is not valid")
    exit()

if args.id == None:
    print("Please specify the id of the verification")
    exit()

# TODO : Check if the id is valid

verification = Verification(args.path)

