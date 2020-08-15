#!/usr/bin/python3
import os
from re import search
from sys import argv

from Dirr import Dirr
from utils import roundsSize
from styling import S, T, Bg, stylizesStr

TAB = ' ' * 4
fullDataFolders = list()

FILE, FOLDER = "file", "folder"
def printsTree(name, type, idtPrev, pathPos, amtPrevDirrPaths, size=None):
	idt = idtPrev
	dots = stylizesStr(":", T.red, s1=S.strong)
	if pathPos == amtPrevDirrPaths:
		idt = "{}{}{}".format(idt, TAB, " ")
	else:
		idt = "{}{}{}".format(idt, TAB, dots)

	arrowIdt = "{}{}".format(idtPrev, TAB)

	if type == FOLDER:
		if name[0] != '/':
			name = "/{}".format(name)
		name = stylizesStr(name, T.purple, s1=S.strong, s2=S.italic)

		arrow = "`--> "
		arrow = stylizesStr(arrow, T.red, s1=S.strong)
		print("{}{}{}".format(arrowIdt, arrow, name))
	elif type == FILE:
		name = stylizesStr(name, T.purple)
		size = roundsSize(size)
		size = stylizesStr(size, T.cyan, s1=S.strong)

		arrow = "`-> "
		arrow = stylizesStr(arrow, T.red, s1=S.strong)
		text = stylizesStr(" has usage ", s1=S.blur, s2=S.italic)

		print("{}{}{}{}{}".format(arrowIdt, arrow, name, text, size))

		if amtPrevDirrPaths == pathPos: print(arrowIdt)

	return idt

def analyzesIgnoredDirr(entry, name, nv, amtIgnr, ignrSize):
	newAmtIgnr, newIgnrS = 0, 0
	if os.path.isdir(entry):
		newAmtIgnr, newIgnrS, _, _, _, _ = analyzesMem(entry.path, nv+1)
	elif os.path.isfile(entry):
		newIgnrS = os.path.getsize(entry)

	if name[0] == '.':
		newAmtIgnr += 1

	return amtIgnr + newAmtIgnr, ignrSize + newIgnrS

def analyzesMem(path, nv, amtPrevDirrPaths=1, idtPrev=" ", pathPos=1):
	ignore = r"/\."
	folderName = os.path.basename(path)
	isIgnr = search(ignore, path)

	amtIgnr, amtFolders, amtFiles = 0, 0, 0
	for entry in os.scandir(path):
		name = os.path.basename(entry)

		if search(ignore, entry.path):
			continue

		if os.path.isdir(entry):
			amtFolders += 1
		elif os.path.isfile(entry):
			amtFiles += 1
	amtPrevDirrPaths = amtFolders + amtFiles

	amtSubFolders, amtSubFiles = 0, 0
	ignrSize, notIgnrSize = 0, 0
	for entry in os.scandir(path):
		name = os.path.basename(entry)

		if search(ignore, entry.path):
			amtIgnr, ignrSize = analyzesIgnoredDirr(entry, name, nv, amtIgnr, ignrSize)
			continue

		if os.path.isdir(entry):
			idt = printsTree(name, FOLDER, idtPrev, pathPos, amtPrevDirrPaths)
			# analyzesSubFolder()
			amtIgnrF, ignrS, amtSubFo, amtSubFi, notIgnrS, _ = analyzesMem(entry.path, nv+1, amtPrevDirrPaths, idt)
			amtIgnr += amtIgnrF

			amtSubFolders += amtSubFo
			amtSubFiles += amtSubFi

			ignrSize += ignrS
			notIgnrSize += notIgnrS

		elif os.path.isfile(entry):
			size = os.path.getsize(entry)
			notIgnrSize += size

			printsTree(name, FILE, idtPrev, pathPos, amtPrevDirrPaths, size)

		pathPos += 1

	if not isIgnr:
		folderData = Dirr(nv, folderName, amtIgnr, ignrSize, amtFolders, amtSubFolders, amtSubFiles, amtFiles, notIgnrSize)
		fullDataFolders.append(folderData)

	return amtIgnr, ignrSize, amtSubFolders + amtFolders, amtSubFiles + amtFiles, notIgnrSize, amtFolders

def getsInputPath(path):
	workingPath = os.getcwd()
	dirr = "{}/{}".format(workingPath, path)

	if not os.path.exists(dirr):
		print("Bad inpuT. Try again with path to a existing directory.")
		exit()
	elif not os.path.isdir(dirr):
		print("Bad inpuT. Try again with path to a directory.")
		exit()

	os.chdir(path)
	dirr = os.getcwd()

	return dirr

def validatesInput():
	if len(argv) > 2:
		print("Bad inpuT. Try again with:")
		print(" \"./diskanalyzesMem <path>\" or only \"./diskanalyzesMem\" for analize current directory.")
		exit()

	dirr = "/home"
	if len(argv) == 2:
		dirr = getsInputPath(argv[1])

	return dirr

def printHeaderTree(directory, terminalWidth):
	name = "/{}".format(os.path.basename(directory))
	name = stylizesStr(name, T.purple, s1=S.strong, s2=S.italic)

	edge = ' - ' * (terminalWidth // 6 - 1)
	title = "{}|TREE|{}".format(edge[1:], edge[:-1])
	title = stylizesStr(title, T.cyan)

	arrow = "`--> "
	arrow = stylizesStr(arrow, T.red, s1=S.strong)
	print("\n{}".format(title))
	print("{}{}".format(arrow, name))

def printsDataTree(terminalWidth):
	edge = ' - ' * (terminalWidth // 6 - 1)
	title = "{}|DATA TREE|{}".format(edge[4:], edge[:-1])
	title = stylizesStr(title, T.cyan, s1=S.strong)

	print("\n\n{}".format(title))
	for folder in fullDataFolders[::-1]: print(folder, end="")

def main():
	directory = validatesInput()
	terminalWidth = int(os.popen('stty size', 'r').read().split()[1])

	printHeaderTree(directory, terminalWidth)
	analyzesMem(directory, 1)
	printsDataTree(terminalWidth)

if __name__ == "__main__":
	main()