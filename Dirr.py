from utils import roundsSize
from styling import S, T, Bg, stylizesStr

TAB = ' ' * 4

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
		header = "{}".format(idt)

		name = stylizesStr(self.name, T.red, s1=S.strong)
		initP1 = len(self.name) // 2
		initP2 = len(self.name) - initP1

		bar = stylizesStr("\\", T.cyan, s1=S.strong)
		p1 = "{}{}{}".format(bar, (17 - initP1) * detail, " ")
		p2 = "{}{}".format(" ", (19 - initP2) * detail)

		if self.amtFolders == 0 and self.amtFiles == 0 and self.amtIgnr == 0:
			title = "\n{}{}{}{}\n".format(idt, p1, name, p2)
			emptyMsg = "{}{:^40}\n".format(idt, "This directory is empty :(")
		else:
			if self.lv == 1: title = "{}{}{}{}\n{}{}\n".format(idt, p1, name, p2, idt + TAB, pipe)
			else: title = "\n{}{}{}{}\n{}{}\n".format(idt, p1, name, p2, idt + TAB, pipe)

			idt += TAB
			doubleArrow = stylizesStr(">> ", T.cyan, s1=S.strong)

			text = stylizesStr("Total size", txt=T.red, s1=S.strong)
			totalSize = "{}{}{}            {}{}\n".format(idt, pipe, text, doubleArrow, self.totalSize)

			sep = '¨' * 34
			sep = stylizesStr(sep, T.cyan, s1=S.strong)

			if self.amtIgnr > 0:
				sep1 = "{}{}{}\n".format(idt, pipe, sep)

				text = stylizesStr("Ignored's amount", txt=T.red, s1=S.strong)
				ignr = "{}{}{}      {}{}\n".format(idt, pipe, text, doubleArrow, self.amtIgnr)

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