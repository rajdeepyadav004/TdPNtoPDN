from nets import tdpn, pdn
import sys
from itertools import product, permutations

DEBUG=False;



def divide(trans):
	#helper function in the transition

	inArcs = []
	for arc in trans[1]:

		lst = []
		if arc[1] and arc[1] != "singular":

			endpoints = arc[2]
			for i in range(endpoints[0], endpoints[1]):
				lst.append((arc[0], "singular", i, arc[3]))
				lst.append((arc[0], "interval", i, arc[3]))

			if arc[1] == "closed":
				lst.append((arc[0], "singular", endpoints[1], arc[3]))

			elif arc[1] == "leftOpen":
				lst.append((arc[0], "singular", endpoints[1], arc[3]))
				lst.pop(0)

			elif arc[1] == "open":
				lst.pop(0)


		elif arc[1] and arc[1]=="singular":
			lst = [(arc[0], "singlular", arc[2][0],arc[3])]


		else:
			lst = [arc[0], None, None, arc[3]]
		inArcs.append(lst)


	return [list(x) for x in  product(*inArcs)]
### END OF HELPER FUNCTION "divide()" ####


def sortArcs(timedNet):
	# helper function to sort timedNet arcs
	for item in timedNet.transitions:
		arcs = item[1]
		if arcs:
			arcs.sort(reverse=True, key = lambda x: x[1])
			arcs.sort(reverse=False, key = lambda x: x[2])
	### END OF FOR LOOP ###

	return timedNet
### END OF HELPER FUNCTION ###


def modifyTimedNet(timedNet):
	# hepler function to modify timedNet to make it processable
	newTransitions = []

	for trans in timedNet.transitions:

		inArc, outArc = trans[1],[]
		counter = 1

		for arc in trans[2]:

			if arc[1] and arc[1]!="singular":
				var = (trans[0] + ".X" + str(counter))
				inArc.append(("storage", arc[1], arc[2],var))
				outArc.append((arc[0], None, None, var))
				timedNet.data.append(var)

			else:
				outArc.append(arc)

		newTransitions.append((trans[0], inArc, outArc))
	### END OF FOR LOOP ###

	timedNet.places.extend(["storage", "infinity"])
	timedNet.transitions = newTransitions + [("producer", [], [("storage", "singular",[0],None)])]
	producerArcs = []

	for place in timedNet.initMarking.keys():
		producerArcs.append((place, "singular", [0], None))
		timedNet.initMarking[place] = []
	### END OF FOR LOOP ###


	#intermediate step 2
	timedNet.transitions = [item for sublist in list(map(lambda x: (list(map(lambda y: (x[0]+"."+str(y[0]+1),y[1],x[2]),enumerate(divide(x))))) , timedNet.transitions)) for item in sublist]
	timedNet.transitions.append(("massProducer", [("infinity", None, None, None)], producerArcs))	
	timedNet.initMarking["infinity"] = [1]


	##ASERTION###
	file = open("tests/first.test","r")
	contents = file.read()
	file.close()
	assert str(timedNet)+"\n" == contents, '''Error in duplication'''


	#Sorting
	timedNet = sortArcs(timedNet)

	return timedNet
### END OF HELPER FUNCTION "modifyTimedNet" ###


def timeElapseTransitions(timedNet,maximal):
	# Time elapse transitions 
	#el0
	inpMat = {"disc": {"el0.disc": 1, "el0.X":0, "el0.Y":0}, "high": {"el0.disc": 0, "el0.X":1, "el0.Y":0}, "time0": {"el0.disc": 0, "el0.X":0, "el0.Y":0}}
	outMat = {"disc": {"el0.disc": 0, "el0.X":0, "el0.Y":0}, "high": {"el0.disc": 0, "el0.X":0, "el0.Y":1}, "time0": {"el0.disc": 1, "el0.X":0, "el0.Y":0}}
	transitions = [(["disc","high","time0"], ["el0.disc","el0.X","el0.Y"], inpMat, outMat)]

	#el1
	inpMat = {"int":{"el1.disc": 0, "el1.X": 0, "el1.Y": 1}, "time0":{"el1.disc": 1, "el1.X": 0, "el1.Y": 0}, "time1":{"el1.disc": 0, "el1.X": 0, "el1.Y": 0}}
	outMat = {"int":{"el1.disc": 0, "el1.X": 1, "el1.Y": 0}, "time0":{"el1.disc": 0, "el1.X": 0, "el1.Y": 0}, "time1":{"el1.disc": 1, "el1.X": 0, "el1.Y": 0}}
	transitions.append((["time0","int","time1"],["el1.X","el1.Y","el1.disc"],inpMat, outMat))

	#el2
	inpMat = {"disc":{"el2.disc": 0}, "time1":{"el2.disc": 1}}
	outMat = {"disc":{"el2.disc": 1}, "time1":{"el2.disc": 0}}
	transitions.append((["disc", "time1"], ["el2.disc"], inpMat, outMat))

	#el3
	inpMat={"time1": {"el3.disc": 1}, "time2": {"el3.disc": 0}}
	outMat={"time1": {"el3.disc": 0}, "time2": {"el3.disc": 1}}
	transitions.append((["time1", "time2"], ["el3.disc"], inpMat, outMat))

	#el4
	inpMat={
		"time2":{"el4.disc": 1,"el4.X": 0, "el4.Y": 0, "el4.Z": 0},
		"low":{"el4.disc": 0,"el4.X": 1, "el4.Y": 0, "el4.Z": 0},
		"disc": {"el4.disc": 0,"el4.X": 0, "el4.Y": 0, "el4.Z": 0},
		"high": {"el4.disc": 0,"el4.X": 0, "el4.Y": 0, "el4.Z": 1}
	}
	outMat={
		"time2":{"el4.disc": 0,"el4.X": 0, "el4.Y": 0, "el4.Z": 0},
		"low":{"el4.disc": 0,"el4.X": 0, "el4.Y": 1, "el4.Z": 0},
		"disc":{"el4.disc": 1,"el4.X": 0, "el4.Y": 0, "el4.Z": 0},
		"high":{"el4.disc": 0,"el4.X": 0, "el4.Y": 0, "el4.Z": 1}
	}
	transitions.append((["time2", "low", "high", "disc"], ["el4.disc", "el4.X", "el4.Y", "el4.Z"], inpMat, outMat))

	# Defining transitions tf.p.k, tf.p.max, ti.p.k for each place
	newPlaces = []
	for place in timedNet.places:

		newPlaces = newPlaces + list(map(lambda x: place + "." + str(x), (list(range(0,maximal+1))+["inf"])))
		#tf.p.k
	
		for k in range(maximal):
			transName = "tr."+place+"."+str(k)
			inpMat = {
				"high":{transName+".X":0, transName+".Y":1, transName+".disc":0},
				"time0":{transName+".X":0, transName+".Y":0, transName+".disc":1},
				"int":{transName+".X":1, transName+".Y":0, transName+".disc":0},
				(place+"."+str(k)):{transName+".X":1, transName+".Y":0, transName+".disc":0}
			}
			outMat = {
				"high":{transName+".X":0, transName+".Y":1, transName+".disc":0},
				"time0":{transName+".X":0, transName+".Y":0, transName+".disc":1},
				"int":{transName+".X":1, transName+".Y":0, transName+".disc":0},
				(place+"."+str(k)):{transName+".X":0, transName+".Y":1, transName+".disc":0}
			}

			transitions.append((["high","int","time0",place+"."+str(k)],[transName+x for x in [".X",".disc",".Y"]],inpMat,outMat))
		### END OF FOR LOOP


		#tf.p.max
		transName = "tf."+place+"."+str(maximal)
		inpMat = {
			"time0":{transName+".disc":1, transName+".X":0},
			"int":{transName+".disc":0, transName+".X":1},
			place+"."+str(maximal):{transName+".disc":0, transName+".X":1},
			place+".inf":{transName+".disc":0, transName+".X":0}
		}
		outMat = {
			"time0":{transName+".disc":1, transName+".X":0},
			"int":{transName+".disc":0, transName+".X":1},
			place+"."+str(maximal):{transName+".disc":0, transName+".X":0},
			place+".inf":{transName+".disc":1, transName+".X":0}
		}
		transitions.append((["time0","int",place+"."+str(maximal), place+".inf"],[transName+x for x in [".X",".disc"]],inpMat,outMat))


		#ti.p.k
		for k in range(maximal):
			transName = "ti."+place+str(k)
			inpMat = {
				"time2":{transName+".X": 0, transName+".Y": 0,transName+".disc": 1},
				"low":	{transName+".X": 0, transName+".Y": 1,transName+".disc": 0},
				"int": {transName+".X": 1, transName+".Y": 0,transName+".disc": 0},
				place+"."+str(k): {transName+".X": 0, transName+".Y": 1,transName+".disc": 0},
				place+"."+str(k+1): {transName+".X": 0, transName+".Y": 0,transName+".disc": 0}
			}
			outMat = {
				"time2":{transName+".X": 0, transName+".Y": 0,transName+".disc": 1},
				"low":	{transName+".X": 0, transName+".Y": 1,transName+".disc": 0},
				"int": {transName+".X": 1, transName+".Y": 0,transName+".disc": 0},
				place+"."+str(k): {transName+".X": 0, transName+".Y": 0,transName+".disc": 0},
				place+"."+str(k+1): {transName+".X": 1, transName+".Y": 0,transName+".disc": 0}
			}
			transitions.append((["time2","low","int",place+"."+str(k),place+"."+str(k+1)],[transName+x for x in [".X",".disc",".Y"]],inpMat,outMat))
		### END OF FOR LOOP ####

	return transitions, newPlaces
### END OF HELPER FUNCTION ###


def discreteTransitions(timedNet, maximal):
	## DISCRETE TRANSTIONS ###
	
	transitions = []
	lst = []
	for trans in timedNet.transitions:

		inpMat = dict()
		outMat = dict()
		data = []
		places = ["int", "low"]
		buff = -1
		temp = None
		num = 0

		for arc in trans[1]:
			if arc:
				datum = None
				if arc[1]!=temp:
					temp = arc[1]
					buff = arc[2]
					data.append([])
					if not arc[3]:
						num += 1
						datum = trans[0] + ".XD" + str(num)
					else:
						datum = arc[3]
					data[-1].append(datum)

				elif arc[1] == temp and arc[1]=="singular" and buff==arc[2]:
					data.append([])
					if not arc[3]:
						datum = trans[0] + ".XD" + str(num)
					else:
						datum = arc[3]
					data[-1].append(datum)

				elif arc[1] == temp and arc[1]=="singular" and buff!=arc[2]:
					buff = arc[2]
					data.append([])
					if not arc[3]:
						num += 1 
						datum = trans[0] + ".XD" + str(num)
					else:
						datum = arc[3]
					data[-1].append(datum)

				elif arc[1] == temp and arc[1]=="interval" and buff == arc[2]:
					if not arc[3]:
						num += 1
						datum = trans[0] + ".XD" + str(num)
					else:
						datum = arc[3]
					data[-1].append(datum)

				elif arc[1] == temp and arc[1]=="interval" and buff != arc[2]:
					buff = arc[2]
					data.append([])
					if not arc[3]:
						num += 1
						datum = trans[0] +".XD"+str(num)
		
					else:
						datum = arc[3]
						data[-1].append(datum)

				else:
					pass

				src = arc[0] + "." + str(arc[2])
				places.append(src)
				inpMat.setdefault(src,{})[datum] = 1
		### END of FOR LOOP ###
		
		for arc in trans[2]:
			if arc:
				dst = None
				iden = None
				try:
					if arc[3] == None:
						dst = arc[0]+"."+arc[2][0]
						iden = trans[0]+".int"
					else:
						for arc1 in trans[1]:
							if arc1:
								if arc1[3] == arc[3]:
									dst = arc[0]+"."+str(arc1[2])
									iden = arc[3]
					places.append(dst)
					outMat.setdefault(dst,{})[iden]=1

				except:
					pass
		### END OF FOR LOOP ###		
			

		inpMat.setdefault("disc",{})[trans[0]+".disc"]=1
		inpMat.setdefault("int",{})[trans[0]+".int"]=1
		inpMat.setdefault("low",{})[trans[0]+".low"]=1

		outMat.setdefault("disc",{})[trans[0]+".disc"]=1
		outMat.setdefault("int",{})[trans[0]+".int"]=1
		outMat.setdefault("low",{})[trans[0]+".low"]=1


		L = [list(permutations(x)) for x in data]
		data =[[item for sub in sublist for item in sub] for sublist in list(product(*L))] 

		for arrange in data:
			for place in places:

				inpMat.setdefault(place,{})
				outMat.setdefault(place,{})

				for datum in [trans[0]+".int",trans[0]+".low"]+arrange:

					inpMat[place].setdefault(datum,0)
					outMat[place].setdefault(datum,0)
				### END OF FOR LOOP ###		
			### END OF FOR LOOP ###		
			lst.append((places, [trans[0]+".int",trans[0]+".low"]+arrange, inpMat, outMat))
		### END OF FOR LOOP ###

	transitions.extend(lst)

	return transitions	
### END OF HELPER FUNCTION ###



def translate(timedNet):
	maximal = 2

	#intermediate step 1
	timedNet = modifyTimedNet(timedNet)

	# declaring a new data net and finding maximal constant
	dataNet = pdn()
	maximal = 2

	#defining places
	dataNet.addPlaces(["int", "low", "high", "disc", "time0", "time1", "time2"])

	## DEFINING TRANSITIONS ###
	# time elapse
	temp = timeElapseTransitions(timedNet, maximal)
	dataNet.addTrans(temp[0])
	dataNet.addPlaces(temp[1])

	# discrete
	dataNet.addTrans(discreteTransitions(timedNet, maximal))

	return dataNet
#### END OF FUNCTION "translate" ###



def main(argv):
	timedNet = tdpn()
	timedNet.places = ["p","q","r","s"]
	timedNet.data = ["X"]
	timedNet.transitions = [("tr1", [("p", "open", [1,2], None), ("q", "singular", [1], "X")], [("r", None, None, "X"), ("s", "open", [1,2], None)])]
	timedNet.initMarking = {"p":[0], "q": [1]}
	timedNet.finalMarking = {"r":[2]}
	d = translate(timedNet)
	print(d)



if __name__ == '__main__':
	main(sys.argv)