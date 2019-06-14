import unittest
from timedToData import translate
from nets import tdpn
from itertools import groupby


class TestTransle(unittest.TestCase):
	def testVarOrder(self):
		'''
		Test that variables are in proper order
		'''

		timedNet = tdpn()
		timedNet.places = ["p","q","r","s"]
		timedNet.data = ["X"]
		timedNet.transitions = [("tr1", [("p", "open", [1,2], None), ("q", "singular", [1], "X")], [("r", None, None, "X"), ("s", "open", [1,2], None)])]
		timedNet.initMarking = {"p":[0], "q": [1]}
		timedNet.finalMarking = {"r":[2]}
		dataNet = translate(timedNet)

		temp = str(dataNet).lower().split("\n")

		temp = filter(lambda x: ("data" in x),temp)

		for line in temp:
			line = filter(lambda x: ("int" in x) or ("disc" in x) or ("low" in x) or ("high" in x), line)
			for x in line:
				if ("int" in x):
					x = 1
				elif ("disc" in x):
					x = 2
				elif ("low" in x):
					x = 3
				elif ("" in x):
					x = 4

			line = [x[0] for x in groupby(line)]
			seq = str([1,2,3]).strip("[]")
			line = str(line).strip("[]")
			self.assertIn(line,seq)

### END OF CLASS ###

if __name__ == "__main__":
	unittest.main()