#!/usr/bin/python3
from re import search
from sys import argv
from math import ceil
import os

MEMREF = 2**10
TAB = ' ' * 4
fullDataFolders = list()

class S: #Style flags
	none = ";0"
	strong = ";1"
	blur = ";2"
	italic = ";3"
	underline = ";4"
	flash = ";6"
	negative = ";7"
	strike = ";9"

class T: #Text Colors flags
	none = ";50"
	black = ";30"
	red = ";31"
	green = ";32"
	yellow = ";33"
	blue = ";34"
	purple = ";35"
	cyan = ";36"
	white = ";37"

class Bg: #Background colors flags
	none = ";50"
	black = ";40"
	red = ";41"
	green = ";42"
	yellow = ";43"
	blue = ";44"
	purple = ";45"
	cyan = ";46"
	white = ";47"

def stylizesStr(string, txt=T.none, bg=Bg.none, s1=S.none, s2=S.none, s3=S.none, s4=S.none, s5=S.none, s6=S.none):
	start = "\033[0{}{}{}{}{}{}{}{}m".format(s6, s5, s4, s3, s2, s1, txt, bg)
	end = "\033[m"
	return "{}{}{}".format(start, string, end)

identifiers = {
	"Data":{
		"Data and database":{
			".csv":"Comma separated value file",
			".dat":"Data file",
			".db":"Database file",
			".dbf":"Database file",
			".log":"Log file",
			".mdb":"Microsoft Access database file",
			".sav":"Save file (e.g., game save file)",
			".sql":"SQL database file",
			".tar":"Linux / Unix tarball file archive",
			".xml":"XML file"
		},
		"Compressed":{
			".7z":"7-Zip compressed file",
			".arj":"ARJ compressed file",
			".deb":"Debian software package file",
			".pkg":"Package file",
			".rar":"RAR file",
			".rpm":"Red Hat Package Manager",
			".tar.gz":"Tarball compressed file",
			".z":"Z compressed file",
			".zip":"Zip compressed file"
		}
	},
	"Docs":{
		"Text":{
			".doc":"Microsoft Word file",
			".docx":"Microsoft Word file",
			".odt":"OpenOffice Writer document file",
			".pdf":"PDF file",
			".rtf":"Rich Text Format",
			".tex":"A LaTeX document file",
			".txt":"Plain text file",
			".wpd":"WordPerfect document"
	},
		"Presentation":{
			".key":"Keynote presentation",
			".odp":"OpenOffice Impress presentation file",
			".pps":"PowerPoint slide show",
			".ppt":"PowerPoint presentation",
			".pptx":"PowerPoint Open XML presentation"
		}
	},
	"Midia":{
		"Videos":{
			".3g2":"3GPP2 multimedia file",
			".3gp":"3GPP multimedia file",
			".avi":"AVI file",
			".flv":"Adobe Flash file",
			".h264":"H.264 video file",
			".m4v":"Apple MP4 video file",
			".mkv":"Matroska Multimedia Container",
			".mov":"Apple QuickTime movie file",
			".mp4":"MPEG4 video file",
			".mpg":"MPEG video file",
			".mpeg":"MPEG video file",
			".rm":"RealMedia file",
			".swf":"Shockwave flash file",
			".vob":"DVD Video Object",
			".wmv":"Windows Media Video file"
		},
		"Images":{
			".ai":"Adobe Illustrator file",
			".bmp":"Bitmap image",
			".gif":"GIF image",
			".ico":"Icon file",
			".jpeg":"JPEG image",
			".jpg":"JPEG image",
			".png":"PNG image",
			".ps":"PostScript file",
			".psd":"PSD image",
			".svg":"Scalable Vector Graphics file",
			".tif":"TIFF image",
			".tiff":"TIFF image"
		},
		"Audio":{
			".aif":"AIF audio file",
			".cda":"CD audio track file",
			".mid":"MIDI audio file",
			".midi":"MIDI audio file",
			".mp3":"MP3 audio file",
			".mpa":"MPEG-2 audio file",
			".ogg":"Ogg Vorbis audio file",
			".wav":"WAV file",
			".wma":"WMA audio file",
			".wpl":"Windows Media Player playlist"
		}
	},
	"Code":{
		".c":"C/C++",
		".class":"Java",
		".cpp":"C++",
		".cs":"Visual C#",
		".h":"C/C++",
		".java":"Java",
		".pl":"Perl script",
		".sh":"Bash shell script",
		".swift":"Swift",
		".vb":"Visual Basic",
		".asp":"Active Server Page",
		".aspx":"Active Server Page",
		".cfm":"ColdFusion Markup",
		".cgi":"Perl script",
		".pl":"Perl script",
		".css":"Cascading Style Sheet",
		".htm":"HTML",
		".html":"HTML",
		".js":"JavaScript",
		".jsp":"Java Server Page",
		".php":"PHP",
		".py":"Python",
		".rss":"RSS",
		".xhtml":"XHTML"
	}
}

def roundsSize(size):
	units = ["B", "KB", "MB", "GB", "TB"]
	i = 0

	while size // (MEMREF ** (i + 1)) > 0:
		i += 1

	size = size / (MEMREF ** i)
	size = "{:.2f} {}".format(size, units[i])

	return size

class Dirr:
	def __init__(self, lv, name, amtIgnr, ignrSize, amtFolders, amtSubFolders, amtSubFiles, amtFiles, notIgnrSize, totalSize=0):
		self.lv = lv
		self.name = name

		self.amtIgnr = amtIgnr
		self.ignrSize = roundsSize(ignrSize)

		self.amtFolders = amtFolders
		self.amtSubFolders = amtSubFolders
		self.amtSubFiles = amtSubFiles

		self.amtFiles = amtFiles
		self.notIgnrSize = roundsSize(notIgnrSize)

		self.totalSize = roundsSize(ignrSize + notIgnrSize)

	def __repr__(self):
		idt = ""
		pipe = stylizesStr("|", T.cyan, s1=S.strong)
		for i in range(self.lv - 1):
			idt += "{}{}".format(TAB, pipe)

		title, emptyMsg, totalSize, sep1, sep2 = "", "", "", "", ""
		ignr, ignrSize = "", ""
		folders, subFolders, subFiles, files, size = "", "", "", "", ""

		detail = stylizesStr('_', T.cyan, s1=S.strong)
		# header = "\n{}{}\n".format(idt, 40 * detail)
		header = "{}".format(idt)

		name = stylizesStr(self.name, T.red, s1=S.strong)
		initP1 = len(self.name) // 2
		initP2 = len(self.name) - initP1

		bar = stylizesStr("\\", T.cyan, s1=S.strong)
		p1 = "{}{}".format(bar, (18 - initP1) * detail)
		p2 = "{}".format((20 - initP2) * detail)


		if self.amtFolders == 0 and self.amtFiles == 0 and self.amtIgnr == 0:
			title = "\n{}{}{}{}\n".format(idt, p1, name, p2)
			emptyMsg = "{}{:^40}\n".format(idt, "This directory is empty :(")
		else:
			title = "\n{}{}{}{}\n{}{}\n".format(idt, p1, name, p2, idt + TAB, pipe)
			idt += TAB
			doubleArrow = stylizesStr(">> ", T.cyan, s1=S.strong)

			text = stylizesStr("Total size", txt=T.red, s1=S.strong)
			totalSize = "{}{}{}            {}{}\n".format(idt, pipe, text, doubleArrow, self.totalSize)

			sep = '¨' * 34
			sep = stylizesStr(sep, T.cyan, s1=S.strong)

			if self.amtIgnr > 0:
				sep1 = "{}{}{}\n".format(idt, pipe, sep)

				text = stylizesStr("Ignored amount", txt=T.red, s1=S.strong)
				ignr = "{}{}{}        {}{}\n".format(idt, pipe, text, doubleArrow, self.amtIgnr)

				text2 = stylizesStr("Ignored data size", txt=T.red, s1=S.strong)
				ignrSize = "{}{}{}     {}{}\n".format(idt, pipe, text2, doubleArrow, self.ignrSize)

			if self.amtFolders > 0 or self.amtFiles > 0:
				sep2 = "{}{}{}\n".format(idt, pipe, sep)

				text = stylizesStr("Data size", txt=T.red, s1=S.strong)
				size = "{}{}{}             {}{}\n".format(idt, pipe, text, doubleArrow, self.notIgnrSize)

				if self.amtFolders > 0:
					text = stylizesStr("Folders' amount", txt=T.red, s1=S.strong)
					folders = "{}{}{}       {}{}\n".format(idt, pipe, text, doubleArrow, self.amtFolders)

					if self.amtSubFolders > 0:
						t1 = stylizesStr(" `->sub folders ", s1=S.blur)
						subFolders = "{}{}{}{}{}\n".format(idt, pipe, t1, doubleArrow, self.amtSubFolders)
					if self.amtSubFiles > 0:
						t2 = stylizesStr(" `->sub files   ", s1=S.blur)
						subFiles = "{}{}{}{}{}\n".format(idt, pipe, t2, doubleArrow, self.amtSubFiles)

				if self.amtFiles > 0:
					text = stylizesStr("Files' amount", txt=T.red, s1=S.strong) 
					files = "{}{}{}         {}{}\n".format(idt, pipe, text, doubleArrow, self.amtFiles)

		return "{}{}{}{}{}{}{}{}{}{}{}{}{}".format(header, title, emptyMsg, totalSize, sep1, ignr, ignrSize, sep2, folders, subFolders, subFiles, files, size)

FILE, FOLDER = "file", "folder"
dots = stylizesStr(":", T.red, s1=S.strong)
def printsTree(name, type, idtPrev, pathPos, amtPaths, size=None):
	idt = idtPrev
	if pathPos == amtPaths:
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

		if amtPaths == pathPos: print(arrowIdt)

	return idt
'''
def anylizesIgnoredFiles():
'''
def analyzesMem(path, nv, amtPaths=1, idtPrev=" ", pathPos=1):
	ignore = r"/\."
	folderName = os.path.basename(path)
	isIgnr = search(ignore, path)

	amtIgnr, amtFolders, amtFiles = 0, 0, 0
	for entry in os.scandir(path):
		name = os.path.basename(entry)

		if search(ignore, entry.path):
			if name[0] == '.':
				amtIgnr += 1
			continue

		if os.path.isdir(entry):
			amtFolders += 1
		elif os.path.isfile(entry):
			amtFiles += 1
	amtPaths = amtFolders + amtFiles

	amtSubFolders, amtSubFiles = 0, 0
	ignrSize, notIgnrSize = 0, 0
	for entry in os.scandir(path):
		name = os.path.basename(entry)

		if search(ignore, entry.path):
			if name[0] == '.':
				amtIgnr += 1

			if os.path.isdir(entry):
				amtIgnrF, ignrS, _, _, _, _ = analyzesMem(entry.path, nv+1)
				amtIgnr += amtIgnrF
				ignrSize += ignrS

			elif os.path.isfile(entry):
				size = os.path.getsize(entry)
				ignrSize += size

			continue

		if os.path.isdir(entry):
			idt = printsTree(name, FOLDER, idtPrev, pathPos, amtPaths)

			amtIgnrF, ignrS, amtSubFo, amtSubFi, notIgnrS, _ = analyzesMem(entry.path, nv+1, amtPaths, idt)
			amtIgnr += amtIgnrF

			amtSubFolders += amtSubFo
			amtSubFiles += amtSubFi

			ignrSize += ignrS
			notIgnrSize += notIgnrS

		elif os.path.isfile(entry):
			size = os.path.getsize(entry)
			notIgnrSize += size

			printsTree(name, FILE, idtPrev, pathPos, amtPaths, size)

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

def printsDataTree(edge):
	title = "{}DATA TREE{}".format(edge[3:], edge[3:])
	title = stylizesStr(title, T.cyan, s1=S.strong)
	print("\n\n{}".format(title))

	for folder in fullDataFolders[::-1]: print(folder, end="")

def validatesInput():
	if len(argv) > 2:
		print("Bad inpuT. Try again with:")
		print(" \"./diskanalyzesMem <path>\" or only \"./diskanalyzesMem\" for analize current directory.")
		exit()

	dirr = "/home"
	if len(argv) == 2:
		dirr = getsInputPath(argv[1])

	return dirr

def main():
	directory = validatesInput()

	name = "/{}".format(os.path.basename(directory))
	name = stylizesStr(name, T.purple, s1=S.strong, s2=S.italic)

	edge = ' - ' * 10
	title = "{}TREE{}".format(edge, edge)
	title = stylizesStr(title, T.cyan)

	arrow = "`--> "
	arrow = stylizesStr(arrow, T.red, s1=S.strong)
	print("\n{}".format(title))
	print("{}{}".format(arrow, name))

	analyzesMem(directory, 1)

	printsDataTree(edge)

if __name__ == "__main__":
	main()

'''
end=f" \033[1;32m{pathPos}º | {amtPaths}\033[m\n"
-  -  -  -  -  -  -  -  -  - TREE -  -  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -  - DATA TREE -  -  -  -  -  -  -  -  -
'''