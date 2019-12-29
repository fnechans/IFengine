#!/usr/bin/env python3

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

yes = ["yes","YES","Yes","y","Y"]

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
        confirmation = input("\n  Are you sure? ")
        if confirmation in yes:
            return True
        else:
            print("\n  I did not understand...")
            return False

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
                if res == "end":
                    print("\n\n--------------------------------------")
                    print("You have escaped! Congratulations!")
                    return True
    elif verb == "use":
        if length < 2:
            print("  Use what on what?")
            return False
        item = inp[1]
        if item not in inventory:
            print("  You do not have " + item + " in inventory.")
            return False
        if length < 3:
            print("  Use " + item + " on what?")
            return False
        pos = 2
        if inp[2] == "on": 
            if length < 4:
                print("  Use " + item + " on what?")
                return False
            pos = 3
        obj = curRoom.get_object(inp[pos])
        if obj == "NONE":
            return False
        obj.use(item)
    elif verb == "look":
        curRoom.describe()
    elif verb == "examine":
        if length == 1:
            print("  Examine what?")
            return False
        if inp[1] in inventory:
            inventory[inp[1]].describe()
            return False 
        curRoom.describe_object(inp[1])
    elif verb == "take":
        obj = curRoom.take_object(inp[1])
        if obj == "NONE":
            return False
        inventory[inp[1]] = obj
    elif verb == "inventory":
        if len(inventory)==0: 
            print("  You have nothing! NOTHING!!!")
            return False
        out = "  You have: "
        for item in inventory:
            out += item + ", "
        print(out)
    elif verb == "help":
        print("Possible commands:")
        print(" * go (where), possible directions:")
        print(" * exit, quits the game")
        print(roomClass.possibleDirections)
        print(" * use (what) [on] (what)")
        print(" * look, describes current room")
        print(" * examine (object), examines object or item in current room or inventory")
        print(" * take (object), takes object and saves to inventory")
        print(" * inventory, lists items in your inventory")
    else: 
        print("  Unknown verb " + verb)
    return False

print("\nYou have awoken in a foreign room. Find a way to escape!\n\n")

load_stuff()

curRoom = rooms["start"]
curRoom.enter()

while True:
	if eval_input(): break