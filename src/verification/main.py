import os
import argparse
from verification import Verification



parser = argparse.ArgumentParser()
parser.add_argument("--path", help="The path of the executable to test")
args = parser.parse_args()
if args.path == None:
    print("Please specify the path of the executable to test")
    exit()
if not os.path.exists(args.path):
    print("The path of the executable to test is not valid")
    exit()

verification = Verification(args.path)

