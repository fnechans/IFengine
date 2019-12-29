
possibleDirections = ["north","east","south","west"]

def init(what,where):
	if what in where:
		return where[what]
	else:
		return ""

class exitClass:

    def __init__(self,properties):
        self.description = properties["Description"]
        self.destination = properties["Destination"]
        self.name = properties["Name"]
        self.isLocked    = False	
        if "Locked" in properties:
            self.isLocked = True
            self.lockItem = properties["Locked"][0]
            self.lockDescription = properties["Locked"][1]
            self.unlockMessageSuccess = properties["Locked"][2]
            self.unlockMessageFail = properties["Locked"][3]

    def  use(self,name):
        if name == self.lockItem:
            print(self.unlockMessageSuccess)
            self.isLocked = False
        else:
            print(self.unlockMessageFail)

    def exit(self):
        if self.isLocked:
            print(self.lockDescription)
            return "Locked"
        else:
            return self.destination

class itemClass:

	def __init__(self,properties):
		self.look = init("l",properties)
		self.description = init("x",properties)
		self.take = init("l",properties)
		self.move = False
		self.moveDescription = "Unmovable"
		if "m" in properties:
			self.move = properties["m"][0]
			self.moveDescription = properties["m"][1]

class roomClass:

    def __init__(self,properties):
        self.title = properties["Title"]
        self.description = properties["Description"]
        # what is in the room
        self.items = {}
        for item in properties["Items"]: # TODO add check for existemce
        	self.items[item] = itemClass(properties["Items"][item])
        # what are the exits fro the room (name)
        self.exits = {}
        for exit in properties["Exits"]: # TODO add check for existemce
        	self.exits[exit] = exitClass(properties["Exits"][exit])
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
            out += self.exits[ex].description + " "
        print(out)

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
        return "NONE"

    def take_object(self,name):
        if name in self.items:
            content = self.items[name]
            del self.items[name]
        return "NONE"

    def get_exit(self,direction):
        direction = direction.lower()
        
        if not direction in possibleDirections:
            print(direction + " is not a valid direction")
            return "err"

        if direction in self.exits:
            return self.exits[direction].exit()
        else:
            print("Cannot go " + direction)