#!/usr/bin/python3
from re import search
from sys import argv
from math import ceil
import os

MEMREF = 2**10
TAB = ' ' * 4
fullDataFolders = list()

class Style:
	def __init__(self):
			self.none = ";0"
			self.strong = ";1"
			self.blur = ";2"
			self.italic = ";3"
			self.underline = ";4"
			self.flash = ";6"
			self.negative = ";7"
			self.strike = ";9"

class TxtColor:
	def __init__(self):
			self.none = ";50"
			self.white = ";30"
			self.red = ";31"
			self.green = ";32"
			self.yellow = ";33"
			self.blue = ";34"
			self.purple = ";35"
			self.cyan = ";36"
			self.grey = ";37"

class BgColor:
	def __init__(self):
			self.none = ";50"
			self.white = ";40"
			self.red = ";41"
			self.green = ";42"
			self.yellow = ";43"
			self.blue = ";44"
			self.purple = ";45"
			self.cyan = ";46"
			self.grey = ";47"

s = Style()
t = TxtColor()
b = BgColor()

def stringStyling(string, txt=t.none, bg=b.none, s1=s.none, s2=s.none, s3=s.none, s4=s.none, s5=s.none, s6=s.none):
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

def roundSize(size):
	units = ["B", "KB", "MB", "GB", "TB"]
	i = 0

	while size // (MEMREF ** (i + 1)) > 0:
		i += 1

	size = size / (MEMREF ** i)
	size = "{:.2f} {}".format(size, units[i])

	return size

class Dirr:
	def __init__(self, lv, name, nIgnr, ignrSize, nFolders, nSubFolders, nSubFiles, nFiles, notIgnrSize, totalSize=0):
		self.lv = lv
		self.name = name

		self.nIgnr = nIgnr
		self.ignrSize = roundSize(ignrSize)

		self.nFolders = nFolders
		self.nSubFolders = nSubFolders
		self.nSubFiles = nSubFiles

		self.nFiles = nFiles
		self.notIgnrSize = roundSize(notIgnrSize)

		self.totalSize = roundSize(ignrSize + notIgnrSize)

	def __repr__(self):
		if self.lv > 3: return ""

		idt = TAB * (self.lv - 1)

		title, emptyMsg, totalSize, sep1, sep2 = "", "", "", "", ""
		ignr, ignrSize = "", ""
		folders, subFolders, subFiles, files, size = "", "", "", "", ""

		detail = stringStyling('_', t.cyan, s1=s.strong)
		header = "\n{}{}\n".format(idt, 40 * detail)
		header = "\n"

		name = stringStyling(self.name, t.red, b.purple, s1=s.strong)
		initP1 = len(self.name) // 2
		initP2 = len(self.name) - initP1

		detail = stringStyling('-', t.cyan, b.purple)
		pipe = stringStyling("|", t.cyan, s1=s.strong)
		p1 = "{}{}".format(pipe, (19 - initP1) * detail)
		p2 = "{}{}".format((19 - initP2) * detail, pipe)

		title = "{}{}{}{}\n\n".format(idt, p1, name, p2)

		if self.nFolders > 0 or self.nFiles or self.nIgnr:
			doubleArrow = stringStyling(">> ", t.cyan, s1=s.strong)

			text = stringStyling("Total size", txt=t.red, s1=s.strong)
			totalSize = "{}{}                 {}{}\n".format(idt, text, doubleArrow, self.totalSize)

			sep = '¨' * 40
			sep = stringStyling(sep, t.cyan, s1=s.strong)

			if self.nIgnr > 0:
				sep1 = "{}{}\n".format(idt, sep)

				text = stringStyling("Ignored amount", txt=t.red, s1=s.strong)
				ignr = "{}{}             {}{}\n".format(idt, text, doubleArrow, self.nIgnr)

				text2 = stringStyling("Ignored data size", txt=t.red, s1=s.strong)
				ignrSize = "{}{}          {}{}\n".format(idt, text2, doubleArrow, self.ignrSize)

			if self.notIgnrSize[0] != '0':
				sep2 = "{}{}\n".format(idt, sep)

				text = stringStyling("Data size", txt=t.red, s1=s.strong)
				size = "{}{}                  {}{}\n".format(idt, text, doubleArrow, self.notIgnrSize)

			if self.nFolders > 0:
				text = stringStyling("Folders' amount", txt=t.red, s1=s.strong)
				folders = "{}{}            {}{}\n".format(idt, text, doubleArrow, self.nFolders)

				if self.nSubFolders > 0:
					t1 = stringStyling("  `->sub folders ", s1=s.blur)
					subFolders = "{}{}{}{}\n".format(idt, t1, doubleArrow, self.nSubFolders)
				if self.nSubFiles > 0:
					t2 = stringStyling("  `->sub files   ", s1=s.strong)
					subFiles = "{}{}{}{}\n".format(idt, t2, doubleArrow, self.nSubFiles)

			if self.nFiles > 0:
				text = stringStyling("Files' amount", txt=t.red, s1=s.strong)
				files = "{}{}              {}{}\n".format(idt, text, doubleArrow, self.nFiles)
		else:
			emptyMsg = "{}{:^40}\n".format(idt, "This directory is empty :(")

		return "{}{}{}{}{}{}{}{}{}{}{}{}{}".format(header, title, emptyMsg, totalSize, sep1, ignr, ignrSize, sep2, folders, subFolders, subFiles, files, size)

def report(path, nv):
	ignore = r"/\."
	folderName = os.path.basename(path)
	isIgnr = search(ignore, path)

	nIgnr = 0
	ignrSize = 0

	nFolders = 0
	nSubFolders = 0
	nSubFiles = 0
	nFiles = 0
	notIgnrSize = 0

	indentation = TAB * nv
	for entry in os.scandir(path):
		name = os.path.basename(entry)

		if search(ignore, entry.path):
			if os.path.isdir(entry):
				if name[0] == '.':
					nIgnr += 1

				_, _, _, _, nIgnrF, ignrS = report(entry.path, nv+1)
				nIgnr += nIgnrF
				ignrSize += ignrS

			elif os.path.isfile(entry):
				size = os.path.getsize(entry)
				ignrSize += size

			continue

		if os.path.isdir(entry):
			name = "/{}".format(name)
			name = stringStyling(name, t.purple, s1=s.strong, s2=s.italic)

			arrow = stringStyling("`--> ", t.red, s1=s.strong)
			print("\n{}{}{}".format(indentation, arrow, name))
			nFolders += 1

			notIgnrS, _, nSubFo, nSubFi, nIgnrF, ignrS = report(entry.path, nv+1)
			notIgnrSize += notIgnrS
			nSubFolders += nSubFo
			nSubFiles += nSubFi
			nIgnr += nIgnrF
			ignrSize += ignrS

		elif os.path.isfile(entry):
			name = stringStyling(name, t.purple)

			size = os.path.getsize(entry)
			sizeStr = roundSize(size)
			sizeStr = stringStyling(sizeStr, t.cyan)

			arrow = stringStyling("`-> ", t.red, s1=s.blur)
			text = stringStyling(" has usage ", s1=s.blur, s2=s.italic)
			print("{}{}{}{}{}".format(indentation, arrow, name, text, sizeStr))

			nFiles += 1
			notIgnrSize += size

	if not isIgnr:
		folderData = Dirr(nv, folderName, nIgnr, ignrSize, nFolders, nSubFolders, nSubFiles, nFiles, notIgnrSize)

		fullDataFolders.append(folderData)

	return notIgnrSize, nFolders, nSubFolders + nFolders, nSubFiles + nFiles, nIgnr, ignrSize

def getInputPath(path):
	workingPath = os.getcwd()
	dirr = "{}/{}".format(workingPath, path)

	if not os.path.exists(dirr):
		print("Bad input. Try again with path to a existing directory.")
		exit()
	elif not os.path.isdir(dirr):
		print("Bad input. Try again with path to a directory.")
		exit()

	os.chdir(path)
	dirr = os.getcwd()

	return dirr

def printDataTree(edge):
	title = "{}DATA TREE{}".format(edge[3:], edge[3:])
	title = stringStyling(title, t.cyan, b.purple, s1=s.strong)
	print("\n\n{}".format(title))
	for folder in fullDataFolders[::-1]: print(folder, end="")

def validInput():
	if len(argv) > 2:
		print("Bad input. Try again with:")
		print(" \"./diskReport <path>\" or only \"./diskReport\" for analize current directory.")
		exit()

	dirr = "/home"
	if len(argv) == 2:
		dirr = getInputPath(argv[1])

	return dirr

def main():
	directory = validInput()

	name = "/{}".format(os.path.basename(directory))
	name = stringStyling(name, t.purple, s1=s.strong, s2=s.italic)

	edge = ' - ' * 10
	title = "{}TREE{}".format(edge, edge)
	title = stringStyling(title, t.red, b.purple, s1=s.strong)

	arrow = "`--> "
	arrow = stringStyling(arrow, t.red, s1=s.strong)
	print("\n{}".format(title))
	print("{}{}".format(arrow, name))

	report(directory, 1)

	printDataTree(edge)

if __name__ == "__main__":
	main()

'''
-  -  -  -  -  -  -  -  -  - TREE -  -  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -  - DATA TREE -  -  -  -  -  -  -  -  -
'''