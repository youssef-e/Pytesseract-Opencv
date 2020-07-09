from Classes.Fields import Fields

class Gender(Fields):
	def __init__(self, line = ""):
		Fields.__init__(self, line)

	#look for the id in the extracted lines using key words to locate it; it returns a str
	def extract(self, line):
		gender = "-1"
		#since the line containing the gender tend to not be read correctly
		#it first look for the line containing the first name, then try
		#to locate the gender in the line below it
		words = line.replace("."," ").split(" ")
		for word in words:
			if(word == "M" or word =="F"):
				gender = word
				break
		return self.set_field(gender)