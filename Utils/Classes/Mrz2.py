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
			while len(result)>36:
				index = result.find('<',20)
				if index != -1:
					result = result[:index] + result[index+1:]
				else:
					break
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
	def synthax_check(self):
		if len(self) != 36 or self.field == "-1":
			error = "Warning: Incorrect lenght : MRZ2"
			print(error)
			return (False,error)
		for c in self.field[27:33]:
			if c < '0' or c > '9' :
				error = "Warning: Incorrect data : MRZ2"
				return (False,error)
		return (True, "")