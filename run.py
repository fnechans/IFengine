from main_objects import roomClass
from main_objects import itemClass
from main_objects import exitClass
import json
import sys
from collections import OrderedDict
try:
    import readline
except:
    pass #readline not available

# l look
# x examine
# m move
# t take
# u use
#Upper case: predefined, lower case: specific
jsonData = {}
rooms = {}
inventory = {}

def read_json( fileName ):
    global jsonData 
    try:
        with open( fileName ) as f:
            jsonData = json.load(f, object_pairs_hook=OrderedDict)
    except ValueError as e:
        print("\nIssue while parsing json file.")
        sys.exit(1)

def load_stuff():
    read_json("rooms.json")

    for room in jsonData["Rooms"]:
        rooms[room] = roomClass(jsonData["Rooms"][room])

def eval_input():
    global curRoom

    inp = input("\n> ").split()
    length = len(inp)
    if length == 0: 
        return False

    verb = inp[0]
    if verb == "exit":
        return True

    print("")

    if verb == "go":
        if length == 1:
            print("Go where?")
            return False
        else: 
            res = curRoom.get_exit(inp[1])
            if res == "err" or res == "Locked":
                return False
            else:
                curRoom = rooms[res]
                curRoom.enter()

    elif verb == "use":
        if length == 1:
            print("Use what on what?")
            return False
        item = inp[1]
        if item not in inventory:
            print("You do not have " + item + " in inventory.")
            return False
        if length == 2:
            print("Use " + item + " on what?")
            return False
        obj = curRoom.get_object(inp[2])
        if obj == "NONE":
            print("No object" + inp[2] + "in the room.")
            return False
        obj.use(item)
    elif verb == "look":
        curRoom.describe()
    elif verb == "examine":
        if length == 1:
            print("Examine what?")
            return False
        obj = curRoom.get_object(inp[1])
        if obj == "NONE":
            print("No object" + inp[1] + "in the room")
            return False
        print(obj.description)
    elif verb == "take":
        obj = curRoom.take_object(inp[1])
        if obj == "NONE":
            print("No object" + inp[1] + "in the room")
            return False
        inventory[inp[1]] = obj
    print("Unknown verb "+verb)
    return False

load_stuff()

curRoom = rooms["start"]
curRoom.enter()

while True:
	if eval_input(): break


#res = curRoom.get_exit("north")
#print(res)
#
#curRoom.exits["north"].use("key")
#
#res = curRoom.get_exit("north")
#print(res)
#
#curRoom = rooms[res]
#curRoom.enter()
