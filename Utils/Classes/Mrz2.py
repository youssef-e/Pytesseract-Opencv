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

	def fname_mrz(self):
		return self.field[13:27]
	def id_nbr_mrz(self):
		return self.field[:12]
	def birthday_mrz(self):
		return self.field[27:33]
	def gender_mrz(self):
		return self.field[34]