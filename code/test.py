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
		timedNet.readFromFile("test1.tpn")
		dataNet = translate(timedNet)

		temp = str(dataNet).lower().split("\n")

		temp = list(filter(lambda x: ("data" in x),temp))

		for line in temp[1:]:
			seq=[]
			for x in line.split():
				if ("int" in x):
					seq.append(1)
				elif ("disc" in x):
					seq.append(2)
				elif ("low" in x):
					seq.append(3)
				elif ("high" in x):
					seq.append(4)
			line = [x[0] for x in groupby(seq)]
			order = [[1],[2],[3],[4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4],[1,2,3],[1,2,4],[1,3,4],[2,3,4],[1,2,3,4]]
			self.assertIn(line,order)

### END OF CLASS ###

if __name__ == "__main__":
	unittest.main()