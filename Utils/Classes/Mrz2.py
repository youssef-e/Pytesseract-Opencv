from Classes.Mrz import Mrz
from Classes.Fields import Fields

class Mrz2(Mrz):

	def extract(self, line):
		line = line.upper()
		word = Fields.clean_alphanum(line)
		result = ""
		if ("-1" not in word):
			#clean the unnecessary caracters from the extracted str
			result = Fields.clean_alphanum(word)
		else:
			result = "-1"
		return self.set_field(result)