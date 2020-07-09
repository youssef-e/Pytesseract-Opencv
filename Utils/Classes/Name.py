from Classes.Fields import Fields

class Name(Fields):

	def __init__(self, line = ""):
		Fields.__init__(self, line)

	def extract(self , line):
		name ="-1"
		cleanedLine=line
		for c in line:
			if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '-') and(c !=" ") and(c!= ":")):
				cleanedLine=cleanedLine.replace(c,"")
		words = cleanedLine.split(":")[len(cleanedLine.split(":"))-1].split(" ")
		k=1
		while(k<=len(words)-1):
			if(len(words[len(words)-k])>2):
				name=words[len(words)-k]
				break
			k = k + 1
		if (name== "Nom" or name == "Mom" or name == "nom" or name == "Non" or name == "non"):
			name="-1"

		return self.set_field(name)

	def word_to_mrz(self):
		result = ""
		for i in range(25):
			if i > len(self):
				result +"<"
			elif c =="'" or c == " ":
				result += "<"
			else:
				result += c
		return result.upper()
