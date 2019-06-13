import xml.etree.ElementTree as ET
import tkinter as tk



class tdpn:


	def __init__(self):
		self.places=[]
		self.data=[]
		self.transitions=[]
		self.initMarking=dict()
		self.finalMarking=dict()
		##transitions are tuples (name, list of arcs coming, list of arc going)
		## each arc is a tuple (place, type, constraint, identifier)


	def addPlaces(self, listOfPlaces):
		self.places = self.places + listOfPlaces

	
	def addTrans(self, listOfTrans):
		self.transitions = self.transitions + listOfTrans


	#assume marking is a dict with keys as places and items as list of ages 
	def addInitMarking(self, marking):
		self.initMarking = marking


	def addFinalMarking(self, marking):
		self.finalMarking = marking


	def __str__(self):

		#print places
		val = "places: " + " ".join(self.places)+"\n"

		#print Transitions
		for trans in self.transitions:

			val += "name: "+ trans[0] + "\n"

			val += "in arcs: " + "\n"
			for arc in trans[1]:
				if arc[1]=="interval":
					val+= "\t"+ " ".join(map(str,(arc[0],arc[1],"("+str(arc[2]) + ","+ str(arc[2]+1) +")", arc[3] )))+"\n"
				else:
					val += "\t" + " ".join(map(str, arc)) + "\n"

			val += "out arcs: \n"
			for arc in trans[2]:
				val += "\t" + " ".join(map(str, arc))  + "\n"

			val+="\n"

		#print markings
		val = val + "Initial Markings: " + "\n"
		count = 0
		for place in self.initMarking.keys():
			count +=1
			val = val + "\t"+ str(count) + ". " + place + ": " + " ".join([str(x) for x in self.initMarking[place]]) + "\n"

		return val


	__repr__ = __str__
	
### END OF CLASS ###		



class pdn:


	def __init__(self):
		self.places=[]
		self.data=[]
		self.transitions=[]
		self.initMarking=dict()
		self.finalMarking=dict()
		## each transition will be a tuple with format(places, data, input matrix, output matrix) with matrices as dict of dict


	def addPlaces(self, listOfPlaces):
		self.places = self.places + listOfPlaces


	def adddata(self, listOfdata):
		self.data = self.data = listOfdata

	
	def addTrans(self, listOfTrans):
		self.transitions = self.transitions + listOfTrans


	#assume marking is a dict with items as list of ages 
	def addInitMarking(self, marking):
		self.initMarking = marking


	def addFinalMarking(self,marking):
		self.finalMarking = marking


	def __str__(self):

		#print places
		val = "places: " + " ".join(self.places)+"\n"

		#print data
		val = val + "data: " + " ".join(self.data) + "\n"

		#print transtions
		for rule in self.transitions:
			val = val + "Rule: \n"
			val = val + "\tplaces: " + " ".join(rule[0]) + "\n" 
			val = val + "\tdata: "
			for datum in rule[1]:
				val = val + "\t{:12}".format(datum)
			val = val +"\n"

			inputMat = rule[2]
			outputMat = rule[3]
			val = val + "\tinput: " + "\n"
			for place in rule[0]:
				val = val + "\t    " +"{:12}".format(place)
				for datum in rule[1]:
					val = val + "\t" + '{:12}'.format(str(inputMat[place][datum]))
				val = val + "\n"

			val = val + "\toutput: " + "\n"
			for place in rule[0]:
				val = val + "\t    "+ "{:12}".format(place)
				for datum in rule[1]:
					val = val + "\t" + '{:12}'.format(str(outputMat[place][datum]))
				val = val + "\n"

		#print marking
		val = val + "Initial Markings: " + "\n"
		count = 0
		for place in self.initMarking.keys():
			count +=1
			val = val + "\t"+ str(count) + ". " + place + ": " + " ".join([str(x) for x in self.initMarking[place]]) + "\n"

		return val

### END OF CLASS ###



if __name__ == '__main__':	
	timedNet = tdpn()
	timedNet.places = ["p","q","r","s"]
	timedNet.data = ["X"]
	timedNet.transitions = [("tr1", [("p", "closed", [1,2], None), ("q", "singular", [1], "X")], [("r", None, None, "X"), ("s", "closed", [1,2], None)])]
	timedNet.initMarking = {"p":[0], "q": [1]}
	timedNet.finalMarking = {"r":[2]}
	print(timedNet)