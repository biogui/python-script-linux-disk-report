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