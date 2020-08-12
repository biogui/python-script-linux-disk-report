#!/usr/bin/python3
from sys import argv
import os

def report(initialPath, nv):
	# if nv == 5: exit()
	for entry in os.scandir(initialPath):
		caule = "\t" * nv

		if os.path.isdir(entry):
			size = os.path.getsize(entry)
			print("{}↳folder {} has usage {} bytes".format(caule, entry.path, size))

			report(entry.path, nv+1)
		elif os.path.isfile(entry):
			size = os.path.getsize(entry)
			print("{}↳file {} has usage {} bytes".format(caule, entry.path, size))

def main():
	if (len(argv) != 2):
		print("Bad input. Try again:")
		print(" $ /diskReport <path>")
		exit()

	directory = argv[1]

	report(directory, 0)



if __name__ == "__main__":
	main()