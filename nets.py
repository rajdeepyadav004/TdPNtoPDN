import xml.etree.ElementTree as ET
import tkinter as tk


class tdpn:
	def __init__(self):
		self.places=[]
		self.transitions=[]
		self.arcs=[]
		self.coordinates=dict()
		self.initMarking=dict()
		##arcs are of the format (type, place, transition, condition)
	
	def addPlaces(self, listOfPlaces):
		self.places = self.places + listOfPlaces
	
	def addTrans(self, listOfTrans):
		self.transitions = self.transitions + listOfTrans

	def addArcs(self, listOfArcs):
		self.arcs = self.arcs + listOfArcs

	def addCoordinates(self, dictOfCoordinates):
		self.coordinates = {**self.coordinates, **dictOfCoordinates}

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

	def display(self):
		master = tk.Tk()
		canvas = tk.Canvas(master, width=1500, height=1000)
		canvas.pack()
		for place in self.places:
			canvas.create_oval(self.coordinates[place][0]+30, self.coordinates[place][1]+20, self.coordinates[place][0]-30, self.coordinates[place][1]-20)
			canvas.create_text(self.coordinates[place][0],self.coordinates[place][1], text=place)

		for trans in self.transitions:
			canvas.create_rectangle(self.coordinates[trans][0]+30, self.coordinates[trans][1]+20, self.coordinates[trans][0]-30, self.coordinates[trans][1]-20)
			canvas.create_text(self.coordinates[trans][0],self.coordinates[trans][1], text=trans)

		for arc in self.arcs:
			x1,y1,x2,y2 = 0,0,0,0
			if arc[0]=='ptot':
				x1,y1 = self.coordinates[arc[1]]
				x2,y2 = self.coordinates[arc[2]]
			else:
				x1,y1 = self.coordinates[arc[2]]
				x2,y2 = self.coordinates[arc[1]]

			if x1+60<x2:
				canvas.create_line(x1+30,y1,x2-30,y2,arrow=tk.LAST)
			elif x1>x2+60 and y1<y2:
				canvas.create_line(x1-30,y1,x2+30,y2,arrow=tk.LAST)
			elif y1>y2:
				canvas.create_line(x1,y1-30,x2,y2_30,arrow=tk.LAST)
			else:
				canvas.create_line(x1,y1+30,x2,y2-30,arrow=tk.LAST)

			canvas.create_text((x1+x2)/2, (y1+y2)/2, text=arc[3])


		tk.mainloop()


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



if __name__ == '__main__':	
	net = tdpn()
	net.addPlaces(["p1", "p2"])
	net.addTrans(["tr1"])
	coordinates = {"p1":(750,350), "p2":(750,650), "tr1":(750,500)}
	arcs = [("ptot", "p1", "tr1", "[2,5]"),("ttop", "p2", "tr1", "[3,7]")]
	net.addArcs(arcs)
	net.addCoordinates(coordinates)
	net.display()

	# net.addDatums(["d1", "d2", "d3", "d4"])
	# rules = []
	# rules = rules + [(["p1", "p2"], ["d1", "d2", "d3"], {"p1":{"d1": 1, "d2": 1, "d3":0}, "p2": {"d1": 0, "d2": 1, "d3":1}}, {"p1": {"d1": 1, "d2": 0, "d3":1}, "p2": {"d1": 0, "d2": 0, "d3":1}})]
	# net.addTrans(rules)
	# print(net)


