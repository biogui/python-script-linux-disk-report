#!/usr/bin/python3
from re import search
from sys import argv
from math import ceil
import os

TAB = ' ' * 4
fullData = list()

class Dirr:
	def __init__(self, lv, name, size, nFiles, nFolders):
		self.lv = lv
		self.name = name
		self.size = size
		self.nFiles = nFiles
		self.nFolders = nFolders

	def __repr__(self):
		idt = TAB * (self.lv - 1)
		sizeInfo = "{}Size              >> {} bytes\n".format(idt, self.size)

		e = ceil((len(sizeInfo) - len(idt) - len(self.name) - 1) / 2)
		edge = '-' * e

		title = "{}{}{}{}\n".format(idt, edge, self.name, edge)
		filesInfo = "{}Amount of files   >> {}\n".format(idt, self.nFiles)
		foldersInfo = "{}Amount of folders >> {}\n".format(idt, self.nFolders)

		return "{}{}{}{}".format(title, sizeInfo, filesInfo, foldersInfo)

def strFromChar(origStr, ref):
	init = 0
	for i, c in enumerate(origStr):
		if c == ref: init = i+1

	return origStr[init:]

def report(path, nv):
	indentation = TAB * nv
	ignore = r"/\."

	folderSize = 0
	nFolders = 0
	nFiles = 0

	for entry in os.scandir(path):
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

	folderName = strFromChar(path, '/')
	folderData = Dirr(nv, folderName, folderSize, nFiles, nFolders)

	fullData.append(folderData)

	return folderSize, nFolders, nFiles

def main():
	if (len(argv) != 2):
		print("Bad input. Try again:")
		print(" $ /diskReport <path>")
		exit()

	directory = argv[1]
	name = strFromChar(directory, '/')

	edge = ' - ' * 9
	print("\n- {}TREE{} -".format(edge, edge))
	print("↳/{}".format(name))

	report(directory, 1)

	print("\n\n- {}DATA{} -\n".format(edge, edge))
	for folder in fullData[::-1]: print(folder)


if __name__ == "__main__":
	main()