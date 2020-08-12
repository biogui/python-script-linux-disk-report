#!/usr/bin/python3
from sys import argv
from re import search
import os

def strFromChar(origStr, ref):
	init = 0
	for i, c in enumerate(origStr):
		if c == ref: init = i

	return origStr[init:]

def report(initialPath, nv):
	indentation = "\t" * nv

	ignore = r"/\."

	folderSize = 0
	nFolders = 0
	nFiles = 0

	for entry in os.scandir(initialPath):
		name = os.path.basename(entry)

		if search(ignore, entry.path): continue

		if os.path.isdir(entry):
			print("{}↳/{}".format(indentation, name))
			nFolders += 1

			fS, nFo, nFi = report(entry.path, nv+1)
			folderSize += fS
			nFolders += nFo
			nFiles += nFi

		elif os.path.isfile(entry):
			size = os.path.getsize(entry)
			print("{}↳{} has usage {} bytes".format(indentation, name, size))

			nFiles += 1
			folderSize += size

	return folderSize, nFolders, nFiles

def main():
	if (len(argv) != 2):
		print("Bad input. Try again:")
		print(" $ /diskReport <path>")
		exit()

	directory = argv[1]
	name = strFromChar(directory, '/')

	edge = ' - ' * 10
	print("{}TREE{}".format(edge, edge))
	print("↳/{}".format(name))

	report(directory, 1)



if __name__ == "__main__":
	main()