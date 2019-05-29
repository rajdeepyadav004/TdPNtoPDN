from nets import tdpn, pdn
import sys
def main(argv):
	timedNet = tdpn()
	timedNet.readFromCPN(argv[1])

	print(timedNet)


	print(dataNet)

if __name__ == '__main__':
	main(sys.argv)