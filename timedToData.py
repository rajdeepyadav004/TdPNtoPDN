from nets import tdpn, pdn
import sys
from itertools import product, permutations
import copy

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
	# newTransitions = []

	# for trans in timedNet.transitions:

	# 	inArc, outArc = trans[1],[]
	# 	counter = 1

	# 	for arc in trans[2]:

	# 		if arc[1] and arc[1]!="singular":
	# 			var = (trans[0] + ".X" + str(counter))
	# 			inArc.append(("storage", arc[1], arc[2],var))
	# 			outArc.append((arc[0], None, None, var))
	# 			timedNet.data.append(var)

	# 		else:
	# 			outArc.append(arc)

	# 	newTransitions.append((trans[0], inArc, outArc))
	# ## END OF FOR LOOP ###

	#intermediate step 2
	timedNet.transitions = [item for sublist in list(map(lambda x: (list(map(lambda y: (x[0]+"."+str(y[0]+1),y[1],x[2]),enumerate(divide(x))))) , timedNet.transitions)) for item in sublist]


	##ASERTION###
	# file = open("tests/first.test","r")
	# contents = file.read()
	# file.close()
	# assert str(timedNet)+"\n" == contents, '''Error in duplication'''


	#Sorting
	timedNet = sortArcs(timedNet)

	return timedNet
### END OF HELPER FUNCTION "modifyTimedNet" ###



def timeElapseTransitions(timedNet,maximal):
	# Time elapse transitions 
	#el0
	inpMat = {"disc": {"el0.disc": 1}, "time0": {"el0.disc": 0}}
	outMat = {"disc": {"el0.disc": 0}, "time0": {"el0.disc": 1}}
	transitions = [(["disc"], ["el0.disc"], inpMat, outMat)]

	#el1
	inpMat = {
		"int":{"el1.newInt":0,"el1.oldInt":1,"el1.disc":0,"el1.oldHigh":0,"el1.newHigh":0}, 
		"high":{"el1.newInt":0,"el1.oldInt":0,"el1.disc":0,"el1.oldHigh":1,"el1.newHigh":0},
		"time0":{"el1.newInt":0,"el1.oldInt":0,"el1.disc":1,"el1.oldHigh":0,"el1.newHigh":0}, 
		"time1":{"el1.newInt":0,"el1.oldInt":0,"el1.disc":0,"el1.oldHigh":0,"el1.newHigh":0}
	}
	outMat = {
		"int":{"el1.newInt":1,"el1.oldInt":0,"el1.disc":0,"el1.oldHigh":0,"el1.newHigh":0}, 
		"high":{"el1.newInt":0,"el1.oldInt":0,"el1.disc":0,"el1.oldHigh":0,"el1.newHigh":1},
		"time0":{"el1.newInt":0,"el1.oldInt":0,"el1.disc":0,"el1.oldHigh":0,"el1.newHigh":0}, 
		"time1":{"el1.newInt":0,"el1.oldInt":0,"el1.disc":1,"el1.oldHigh":0,"el1.newHigh":0}
	}
	transitions.append((["int", "high", "time0", "time1"], ["el1.newInt","el1.oldInt","el1.disc","el1.oldHigh","el1.newHigh"],inpMat, outMat))

	#el2
	inpMat = {"disc":{"el2.disc": 0}, "time1":{"el2.disc": 1}}
	outMat = {"disc":{"el2.disc": 1}, "time1":{"el2.disc": 0}}
	transitions.append((["disc", "time1"], ["el2.disc"], inpMat, outMat))

	#el3
	inpMat={"time1": {"el3.disc": 1}, "time2": {"el3.disc": 0}}
	outMat={"time1": {"el3.disc": 0}, "time2": {"el3.disc": 1}}
	transitions.append((["time1", "time2"], ["el3.disc"], inpMat, outMat))

	#yetUnnamedTransition1
	inpMat={
		"low\'":{"YUNT1.low\'":0, "YUNT1.low":0, "YUNT1.high":0},
		"low":{"YUNT1.low\'":0, "YUNT1.low":1, "YUNT1.high":0},
		"high":{"YUNT1.low\'":0, "YUNT1.low":0, "YUNT1.high":1}
	}
	outMat={
		"low\'":{"YUNT1.low\'":1, "YUNT1.low":0, "YUNT1.high":0},
		"low":{"YUNT1.low\'":0, "YUNT1.low":0, "YUNT1.high":0},
		"high":{"YUNT1.low\'":0, "YUNT1.low":0, "YUNT1.high":1}
	}
	transitions.append((["low","low\'","high"],["YUNT1.low\'","YUNT1.low","YUNT1.high"],inpMat,outMat))

	#yetUnnamedTransition2
	inpMat={
		"low\'":{"YUNT2.low":0},
		"low":{"YUNT2.low":1}
	}
	outMat={
		"low\'":{"YUNT2.low":1},
		"low":{"YUNT2.low":0}
	}
	transitions.append((["low\'", "low"],["YUNT2.low"],inpMat,outMat))

	#el4
	inpMat={
		"time2":{"el4.disc":1, "el4.oldLow":0, "el4.newLow":0, "el4.high":0},
		"low":{"el4.disc":0, "el4.oldLow":1, "el4.newLow":0, "el4.high":0},
		"high": {"el4.disc":0, "el4.oldLow":0, "el4.newLow":0, "el4.high":1},
		"disc":{"el4.disc":0, "el4.oldLow":0, "el4.newLow":0, "el4.high":0}
	}
	outMat={
		"time2":{"el4.disc":0, "el4.oldLow":0, "el4.newLow":0, "el4.high":0},
		"low":{"el4.disc":0, "el4.oldLow":0, "el4.newLow":1, "el4.high":0},
		"high":{"el4.disc":0, "el4.oldLow":0, "el4.newLow":0, "el4.high":1},
		"disc":{"el4.disc":1, "el4.oldLow":0, "el4.newLow":0, "el4.high":0}
	}
	transitions.append((["time2", "low", "high", "disc"], ["el4.disc", "el4.oldLow", "el4.newLow", "el4.high"], inpMat, outMat))

	# Defining transitions tf.p.k, tf.p.max, ti.p.k for each place
	newPlaces = []
	for place in timedNet.places:

		newPlaces = newPlaces + list(map(lambda x: place + "." + str(x), (list(range(0,maximal+1))+["inf"])))
		#tf.p.k
	
		for k in range(maximal):
			transName = "tr."+place+"."+str(k)
			inpMat = {
				"high":{transName+".int":0, transName+".high":1, transName+".disc":0},
				"time0":{transName+".int":0, transName+".high":0, transName+".disc":1},
				"int":{transName+".int":1, transName+".high":0, transName+".disc":0},
				(place+"."+str(k)):{transName+".int":1, transName+".high":0, transName+".disc":0}
			}
			outMat = {
				"high":{transName+".int":0, transName+".high":1, transName+".disc":0},
				"time0":{transName+".int":0, transName+".high":0, transName+".disc":1},
				"int":{transName+".int":1, transName+".high":0, transName+".disc":0},
				(place+"."+str(k)):{transName+".int":0, transName+".high":1, transName+".disc":0}
			}

			transitions.append((["high","int","time0",place+"."+str(k)],[transName+x for x in [".int",".disc",".high"]],inpMat,outMat))
		### END OF FOR LOOP


		#tf.p.max
		transName = "tf."+place+"."+str(maximal)
		inpMat = {
			"time0":{transName+".disc":1, transName+".int":0},
			"int":{transName+".disc":0, transName+".int":1},
			place+"."+str(maximal):{transName+".disc":0, transName+".int":1},
			place+".inf":{transName+".disc":0, transName+".int":0}
		}
		outMat = {
			"time0":{transName+".disc":1, transName+".int":0},
			"int":{transName+".disc":0, transName+".int":1},
			place+"."+str(maximal):{transName+".disc":0, transName+".int":0},
			place+".inf":{transName+".disc":1, transName+".int":0}
		}
		transitions.append((["time0","int",place+"."+str(maximal), place+".inf"],[transName+x for x in [".int",".disc"]],inpMat,outMat))


		#ti.p.k
		for k in range(maximal):
			transName = "ti."+place+str(k)
			inpMat = {
				"time2":{transName+".int": 0, transName+".low": 0,transName+".disc": 1},
				"low\'":	{transName+".int": 0, transName+".low": 1,transName+".disc": 0},
				"int": {transName+".int": 1, transName+".low": 0,transName+".disc": 0},
				place+"."+str(k): {transName+".int": 0, transName+".low": 1,transName+".disc": 0},
				place+"."+str(k+1): {transName+".int": 0, transName+".low": 0,transName+".disc": 0}
			}
			outMat = {
				"time2":{transName+".int": 0, transName+".low": 0,transName+".disc": 1},
				"low\'":	{transName+".int": 0, transName+".low": 1,transName+".disc": 0},
				"int": {transName+".int": 1, transName+".low": 0,transName+".disc": 0},
				place+"."+str(k): {transName+".int": 0, transName+".low": 0,transName+".disc": 0},
				place+"."+str(k+1): {transName+".int": 1, transName+".low": 0,transName+".disc": 0}
			}
			transitions.append((["time2","low\'","int",place+"."+str(k),place+"."+str(k+1)],[transName+x for x in [".int",".disc",".low"]],inpMat,outMat))
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

	maximal = 0
	for trans in timedNet.transitions:
		for arc in trans[1]+trans[2]:
			if arc[2]:
				maximal = max(maximal, arc[2][-1])

	#intermediate step 1
	timedNet = modifyTimedNet(timedNet)

	# declaring a new data net and finding maximal constant
	dataNet = pdn()
	

	#defining places
	dataNet.addPlaces(["int", "low", "low\'", "high", "disc", "time0", "time1", "time2", "success"])

	## DEFINING TRANSITIONS ###
	# time elapse
	temp = timeElapseTransitions(timedNet, maximal)
	dataNet.addTrans(temp[0])
	dataNet.addPlaces(temp[1])

	# discrete
	dataNet.addTrans(discreteTransitions(timedNet, maximal))

	id1, id2, id3 = 10, 20, 30


	initMarking = dict()

	initMarking["int"] = [id1]
	initMarking["disc"] = [id2]
	initMarking["low"] = [id3]
	initMarking["high"] = [id3]

	for place in timedNet.initMarking.keys():
		for token in timedNet.initMarking[place]:
			if token<=maximal:
				initMarking.setdefault(place+"."+str(token), [])
				initMarking[place+"."+str(token)].append(id1)
			else:
				initMarking.setdefault(place+".inf", [])
				initMarking[place+".inf"].append(id1)

	tempPlaces = []
	inpMat = dict()
	outMat = dict()

	for place in dataNet.places:
		inpMat[place] = {"int": 0}
		outMat[place] = {"int": 0}

	outMat["success"]["int"] = 1

	for place in timedNet.finalMarking.keys():
		for token in timedNet.finalMarking[place]:
			if token<=maximal:
				tempPlaces.append(place+"."+str(token))
				inpMat[place+"."+str(token)]["int"]+=1
			else:
				tempPlaces.append(places+".inf")
				inpMat[place+".inf"]["int"]+=1

	dataNet.addTrans([(tempPlaces, ["int"], inpMat, outMat)])

	dataNet.addInitMarking(initMarking)
	dataNet.addFinalMarking({"success": [id1]})

	return dataNet
#### END OF FUNCTION "translate" ###



def main(argv):
	timedNet = tdpn()
	timedNet.places = ["p","q","r","s"]
	timedNet.data = ["X"]
	timedNet.transitions = [("tr1", [("p", "open", [1,2], None), ("q", "singular", [1], "X")], [("r", None, None, "X"), ("s", "open", [1,2], None)])]
	timedNet.initMarking = {"p":[0], "q": [1]}
	timedNet.finalMarking = {"r":[2]}

	t2 = tdpn()
	t2.readFromFile("test1.tpn")
	t2.data = ["X"]
	
	d = translate(t2)
	print(d)
	# print(str(t2))


	# print(d2)



if __name__ == '__main__':
	main(sys.argv)