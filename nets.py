import xml.etree.ElementTree as ET


class tdpn:
	def __init__(self):
		self.places=[]
		self.transitions=[]
		self.arcs=[]
		self.initMarking=dict()
		##arcs are of the format (type, place, transition, condition)
	
	def addPlaces(self, listOfPlaces):
		self.places = self.places + listOfPlaces
	
	def addTrans(self, listOfTrans):
		self.transitions = self.transitions + listOfTrans

	def addArcs(self, listOfArcs):
		self.arcs = self.arcs + listOfArcs

	#assume marking is a dict with items as list of ages 
	def addInitMarking(self, marking):
		self.initMarking = marking

	def __str__(self):
		val = "places: " + " ".join(self.places)+"\n"
		val = val + "transitions: " + " ".join(self.transitions)+"\n"
		val = val + "arcs: \n"
		count = 0
		for arc in self.arcs:
			count += 1
			val = val + "\t" + str(count) + ".\n"
			val = val + "\t  type: " + arc[0] + "\n"
			val = val + "\t  place: " + arc[1] + "\n"
			val = val + "\t  transition: " + arc[2] + "\n" 
			val = val + "\t  conditions: " + arc[3] + "\n"

		val = val + "Initial Markings: " + "\n"
		count = 0
		for place in self.initMarking.keys():
			count +=1
			val = val + "\t"+ str(count) + ". " + place + ": " + " ".join([str(x) for x in self.initMarking[place]]) + "\n"

		return val

	def readFromCPN(self, fileName):
		root = ET.parse(fileName).getroot()
		places = root.findall("cpnet/page/place")
		transitions = root.findall("cpnet/page/trans")
		arcs = root.findall("cpnet/page/arc")

		IDtoPlace = {place.attrib["id"]:place.find("text").text for place in places} 
		IDtoTrans = {trans.attrib["id"]:trans.find("text").text for trans in transitions}

		self.addPlaces([(place.find("text").text)  for place in places])
		self.addTrans([(trans.find("text").text) for trans in transitions])
		self.addArcs([(arc.attrib["orientation"], IDtoPlace[arc.find("placeend").attrib["idref"]], IDtoTrans[arc.find("transend").attrib["idref"]], arc.find("annot/text").text) for arc in arcs])


class pdn:
	def __init__(self):
		self.places=[]
		self.datums=[]
		self.transitions=[]
		self.initMarking=dict()
		## each transition will be a tuple with format(places, datums, input matrix, output matrix) with matrices as dict of dict


	def addPlaces(self, listOfPlaces):
		self.places = self.places + listOfPlaces

	def addDatums(self, listOfDatums):
		self.datums = self.datums = listOfDatums
	
	def addTrans(self, listOfTrans):
		self.transitions = self.transitions + listOfTrans

	#assume marking is a dict with items as list of ages 
	def addInitMarking(self, marking):
		self.initMarking = marking

	def __str__(self):
		val = "places: " + " ".join(self.places)+"\n"
		val = val + "datums: " + " ".join(self.datums) + "\n"
		for rule in self.transitions:
			val = val + "Rule: \n"
			val = val + "\tplaces: " + " ".join(rule[0]) + "\n" 
			val = val + "\tdatums: " + " ".join(rule[1]) + "\n"
			inputMat = rule[2]
			outputMat = rule[3]

			val = val + "\tinput: " + "\n"
			for place in rule[0]:
				val = val + "\t\t"
				for datum in rule[1]:
					val = val + " " + str(inputMat[place][datum])
				val = val + "\n"

			val = val + "\toutput: " + "\n"
			for place in rule[0]:
				val = val + "\t\t"
				for datum in rule[1]:
					val = val + " " + str(outputMat[place][datum])
				val = val + "\n"

		val = val + "Initial Markings: " + "\n"
		count = 0
		for place in self.initMarking.keys():
			count +=1
			val = val + "\t"+ str(count) + ". " + place + ": " + " ".join([str(x) for x in self.initMarking[place]]) + "\n"

		return val


net = pdn()

net.addPlaces(["p1", "p2"])
net.addDatums(["d1", "d2", "d3", "d4"])

rules = []
rules = rules + [(["p1", "p2"], ["d1", "d2", "d3"], {"p1":{"d1": 1, "d2": 1, "d3":0}, "p2": {"d1": 0, "d2": 1, "d3":1}}, {"p1": {"d1": 1, "d2": 0, "d3":1}, "p2": {"d1": 0, "d2": 0, "d3":1}})]
net.addTrans(rules)
print(net)