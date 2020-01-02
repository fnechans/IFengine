

def init(what,where):
	if what in where:
		return where[what]
	else:
		return ""

class exitClass:

    def __init__(self,name,properties):
        self.direction = name
        self.look = properties["l"]
        self.description = properties["x"]
        self.destination = properties["Destination"]
        self.name = properties["Name"]
        self.items = {}

        self.isLocked    = False    
        if "Locked" in properties:
            self.isLocked = True
            self.lockItem = properties["Locked"][0]
            self.lockDescription = properties["Locked"][1]
            self.unlockMessageSuccess = properties["Locked"][2]
            self.unlockMessageFail = properties["Locked"][3]
            self.unlockedDescription = properties["Locked"][4]

    def describe(self):
        out = "  "
        out += self.description
        print(out)

    def  use(self,name):
        if name == self.lockItem:
            print("  "+self.unlockMessageSuccess)
            self.isLocked = False
            self.description = self.unlockedDescription
        else:
            print("  "+self.unlockMessageFail)

    def exit(self):
        if self.isLocked:
            print("  "+self.lockDescription)
            return "Locked"
        else:
            return self.destination

class itemClass:

    def __init__(self,name,properties):
        self.name = name
        self.look = init("l",properties)
        self.description = init("x",properties)
        self.move = False
        self.moveDescription = "You cannot move " + name + " or moving it won't do anything"

        # what is in the object
        self.items = {}
        if "Items" in properties:
            for item in properties["Items"]:
                self.items[item] = itemClass(item,properties["Items"][item])

        if "m" in properties:
            self.move = properties["m"][0]
            self.moveDescription = properties["m"][1]

        self.take = False
        self.takeDescription = "You cannot take " + name

        if "t" in properties:
            self.take = properties["t"][0]
            self.takeDescription = properties["t"][1]

        self.isLocked    = False    
        if "Locked" in properties:
            self.isLocked = True
            self.lockItem = properties["Locked"][0]
            self.lockDescription = properties["Locked"][1]
            self.unlockMessageSuccess = properties["Locked"][2]
            self.unlockMessageFail = properties["Locked"][3]
            self.unlockedDescription = properties["Locked"][4]

    def describe(self):
        out = "  "
        out += self.description

        if not self.isLocked and len(self.items):
            out += "\n\n"
            out += "  "
            for it in self.items:
                out += self.items[it].look + " "
        print(out)

    def delete(self,name):
        if name in self.items:
            del self.items[name]
            for nm,it in self.items.items():
                it.delete(name)

    def  use(self,name):
        if name == self.lockItem:
            print("  "+self.unlockMessageSuccess)
            self.isLocked = False
            self.description = self.unlockedDescription
        else:
            print("  "+self.unlockMessageFail)

class roomClass:
    possibleDirections = ["north","east","south","west"]

    def __init__(self,properties):
        self.title = properties["Title"]
        self.description = properties["Description"]
        # what is in the room
        self.items = {}
        if "Items" in properties:
            for item in properties["Items"]:
                self.items[item] = itemClass(item,properties["Items"][item])
        # what are the exits fro the room (name)
        self.exits = {}
        for exit in properties["Exits"]: # TODO add check for existemce
        	self.exits[exit] = exitClass(exit,properties["Exits"][exit])
        # was this room visited before?
        self.visited = False

    def describe(self):
        out = "  "
        out += self.description + "\n\n"

        out += "  "
        for it in self.items:
            out += self.items[it].look + " "
        out += "\n\n"
        out += "  "
        for ex in self.exits:
            out += self.exits[ex].look + " "
        print(out)

    def describe_object(self,name):
        obj =  self.get_object(name)
        if obj == "NONE":
            return "NONE"
        obj.describe()
        if not obj.isLocked:
            for it in obj.items:
                nameIt = obj.items[it].name
                self.items[nameIt] = obj.items[it]

    def enter(self):
        print(self.title)                                            
        print("--------------------------------------")
        if not self.visited:
            print()
            self.describe()
            self.visited = True

    def get_object(self,name):
        if name in self.items:
            return self.items[name]
        for exDir in self.exits:
            ex = self.exits[exDir]
            if ex.name == name:
                return ex
        print("  No object " + name + " in the room.")
        return "NONE"

    def take_object(self,name):
        if name in self.items:
            content = self.items[name]
            print("  " + content.takeDescription)
            if content.take:
                del self.items[name]
                for nm,it in self.items.items():
                    it.delete(name)
                return content
        else:
            print("  No object " + name + " in the room.")
        return "NONE"

    def get_exit(self,direction):
        direction = direction.lower()
        
        if not direction in roomClass.possibleDirections:
            print("  " + direction + " is not a valid direction")
            return "err"

        if direction in self.exits:
            return self.exits[direction].exit()
        else:
            print("  Cannot go " + direction)
