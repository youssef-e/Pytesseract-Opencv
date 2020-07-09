from Classes.Fields import Fields

class Birthday(Fields):

	def extract(self, line):
		result="-1"
		#since the line containing the birthday tend to not be read correctly
		#it first look for the line containing the first name, then try
		#to locate the birthday in the line below it
		line = Fields.clean_alphanum(line, " ")
		words = line.split(" ")
		clean_line=[]
		for value in words:
			if value !="":
				clean_line.append(value)
		#it then can extract the date
		try:
			result = clean_line[len(clean_line)-3]+" "+clean_line[len(clean_line)-2]+" "+clean_line[len(clean_line)-1]
		except IndexError:
			result="-1"
		else:
			for c in result:
				if((c <'0' or c>'9') and (c!=" ")):
					result=result.replace(c,"")
			if len(result)!= 10:
				result ="-1"
		#however if the image is too small, they may not be any lines below the firstname, it then sends an error
		return self.set_field(result)

	def word_to_mrz (self):
		date = self.split(" ")
		return date[2][2:]+date[1]+date[0]