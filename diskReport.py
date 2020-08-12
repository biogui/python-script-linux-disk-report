#!/usr/bin/python3
from re import search
from sys import argv
from math import ceil
import os

MEMREF = 2**10
TAB = ' ' * 4
fullDataFolders = list()

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
	def __init__(self, lv, name, nIgnrFolders, ignrSize, nFolders, nSubFolders, nSubFiles, nFiles, notIgnrSize, totalSize=0):
		self.lv = lv
		self.name = name

		self.nIgnrFolders = nIgnrFolders
		self.ignrSize = roundSize(ignrSize)

		self.nFolders = nFolders
		self.nSubFolders = nSubFolders
		self.nSubFiles = nSubFiles

		self.nFiles = nFiles
		self.notIgnrSize = roundSize(notIgnrSize)

		self.totalSize = roundSize(ignrSize + notIgnrSize)

	def __repr__(self):
		idt = TAB * (self.lv - 1)
		totalSize = "{}Total size              >> {}\n".format(idt, self.totalSize)

		e = ceil((len(totalSize) - len(idt) - len(self.name) - 1) / 2) - 1
		edge = '-' * e
		title = "{}{} {} {}\n".format(idt, edge, self.name, edge)

		sep = '¨' * (len(title) - len(idt)-1)
		sep = "{}{}\n".format(idt, sep)

		ignrFolders = "{}Ignored folders' amount >> {}\n".format(idt, self.nIgnrFolders)
		ignrSize = "{}Ignored data size       >> {}\n".format(idt, self.ignrSize)

		folders = "{}Folders' amount         >> {}\n".format(idt, self.nFolders)
		subFolders = "{}  `->sub folders >> {}\n".format(idt, self.nSubFolders)
		subFiles = "{}  `->sub files   >> {}\n".format(idt, self.nSubFiles)
		files = "{}Files' amount           >> {}\n".format(idt, self.nFiles)
		size = "{}Data size               >> {}\n".format(idt, self.notIgnrSize)

		return "{}{}{}{}{}{}{}{}{}{}{}".format(title, totalSize, sep, ignrFolders, ignrSize, sep, folders, subFolders, subFiles, files, size)

		return size


def report(path, nv):
	ignore = r"/\."
	folderName = os.path.basename(path)
	isIgnr = search(ignore, path)

	nIgnrFolders = 0
	ignrFoldersSize = 0

	notIgnrSize = 0
	nFolders = 0
	nSubFolders = 0
	nSubFiles = 0
	nFiles = 0

	indentation = TAB * nv
	for entry in os.scandir(path):
		name = os.path.basename(entry)

		if search(ignore, entry.path):
			if os.path.isdir(entry):
				if name[0] == '.':
					print("{}`--> /{}".format(indentation, name))
					nIgnrFolders += 1

				_, _, _, _, nIgnrF, ignrS = report(entry.path, nv+1)
				nIgnrFolders += nIgnrF
				ignrFoldersSize += ignrS

			elif os.path.isfile(entry):
				size = os.path.getsize(entry)
				ignrFoldersSize += size

			continue

		if os.path.isdir(entry):
			print("{}`--> /{}".format(indentation, name))
			nFolders += 1

			notIgnrS, nSubFo, nSubFi, _, nIgnrF, ignrS = report(entry.path, nv+1)
			notIgnrSize += notIgnrS
			nSubFolders += nSubFo
			nSubFiles += nSubFi
			nIgnrFolders += nIgnrF
			ignrFoldersSize += ignrS

		elif os.path.isfile(entry):
			size = os.path.getsize(entry)
			print("{}`-> {} has usage {}".format(indentation, name, roundSize(size)))

			nFiles += 1
			notIgnrSize += size

	if not isIgnr:
		folderData = Dirr(nv, folderName, nIgnrFolders, ignrFoldersSize, nFolders, nSubFolders, nSubFiles, nFiles, notIgnrSize)

		fullDataFolders.append(folderData)

	return notIgnrSize, nFolders, nSubFolders + nFolders, nSubFiles + nFiles, nIgnrFolders, ignrFoldersSize

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

def main():
	if len(argv) > 2:
		print("Bad input. Try again with:")
		print(" \"./diskReport <path>\" or only \"./diskReport\" for analize current directory.")
		exit()

	directory = "/home"
	if len(argv) == 2:
		directory = getInputPath(argv[1])

	name = os.path.basename(directory)
	edge = ' - ' * 9
	print("\n- {}TREE{} -".format(edge, edge))
	print("`--> /{}".format(name))

	report(directory, 1)

	print("\n\n- {}DATA{} -\n".format(edge, edge))
	for folder in fullDataFolders[::-1]: print(folder)


if __name__ == "__main__":
	main()