import xml.etree.ElementTree as ET
import tkinter as tk
from lark import Lark


def mystring(tree):
	res = ""
	for val in tree.children:
		res += val
	return res


def getMarking(tree):
	lst = tree.children
	key = None
	res = dict()
	for x in lst:
		if repr(x)[6]=="M":
			key = str(x)
			res[key] = []
		else:
			res[key].append(int(str(x)))
	return res

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


	def readFromFile(self, filename):
		grammar = '''
		start: places transitions "initial marking:" marking "final marking:" marking

		places: "places: " MYSTRING*
		transitions: "transitions: " (MYSTRING arc* "END")+

		marking: (MYSTRING ":" NUMBER*)*
		 
		arc: WORD TYPE INTERVAL ID

		ID: (WORD | "None")
		TYPE: ("ptot" | "ttop")
		INTERVAL: ((LEFTBRACKET NUMBER ["," NUMBER] RIGHTBRACKET) | "None")
		MYSTRING: (WORD NUMBER)
		LEFTBRACKET: "["|"("
		RIGHTBRACKET: ")"|"]"

		 %import common.WORD
		 %import common.LETTER
		 %import common.SIGNED_NUMBER -> NUMBER
		 %import common.WS
		 %ignore WS
		'''


		file = open(filename, "r")
		content = file.read()
		file.close()

		parser = Lark(grammar)
		tree= parser.parse(content)

		place, transition, initMark, finalMark = tree.children
		places = [str(x) for x in place.children]


		transitions = [] 


		name=None
		inArc = []
		outArc = []
		for x in transition.children:
			if(repr(x)[:5]=="Token"):
				transitions.append((name,inArc,outArc))
				name = str(x)
				inArc = []
				outArc = []
			else:
				temp = list(map(str,x.children))
				f = lambda x: inArc if "ptot"==x else outArc
				g = lambda x: None if x=="None" else x

				if temp[2]=="None":
					f(temp[1]).append((temp[0],None,None,g(temp[3])))

				elif not "," in temp[2]:
					f(temp[1]).append((temp[0],"singular",[int(temp[2][1:-1])],g(temp[3])))
				elif temp[2][0]=="(" and temp[2][-1]==")":
					f(temp[1]).append((temp[0],"open",(list(map(int,temp[2][1:-1].split(",")))), g(temp[3])))
				elif temp[2][0]=="(" and temp[2][-1]=="]":
					f(temp[1]).append((temp[0],"leftOpen",(list(map(int,temp[2][1:-1].split(",")))), g(temp[3])))
				elif temp[2][0]=="[" and temp[2][-1]==")":
					f(temp[1]).append((temp[0],"rightOpen",(list(map(int,temp[2][1:-1].split(",")))), g(temp[3])))
				elif temp[2][0]=="[" and temp[2][-1]=="]":
					f(temp[1]).append((temp[0],"closed",(list(map(int,temp[2][1:-1].split(",")))), g(temp[3])))

		transitions.append((name,inArc,outArc))

		if not transitions[0][0]:
			transitions.pop(0)

		self.addPlaces(places)
		self.addTrans(transitions)
		self.addInitMarking(getMarking(initMark))
		self.addFinalMarking(getMarking(finalMark))



	def __str__(self):

		#print places
		val = "places: " + " ".join(self.places)+"\n"

		#print Transitions
		val = val + "transitions: "
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

		val = val + "Final Markings: " + "\n"
		count = 0
		for place in self.finalMarking.keys():
			count +=1
			val = val + "\t"+ str(count) + ". " + place + ": " + " ".join([str(x) for x in self.finalMarking[place]]) + "\n"

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

		val = val + "Final Markings: " + "\n"
		count = 0
		for place in self.finalMarking.keys():
			count +=1
			val = val + "\t"+ str(count) + ". " + place + ": " + " ".join([str(x) for x in self.finalMarking[place]]) + "\n"


		return val

### END OF CLASS ###



if __name__ == '__main__':	
	timedNet = tdpn()
	timedNet.readFromFile("test1.tpn")
	print(timedNet)
