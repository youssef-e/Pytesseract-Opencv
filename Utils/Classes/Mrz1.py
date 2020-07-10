from Classes.Mrz import Mrz
from Classes.Fields import Fields

class Mrz1(Mrz):

	def extract(self, line):
		mrz="-1"
		line = line.upper()
		if("<<" in line and ("IDFRA" in line or "IOFRA" in line or "DFRA" in line or "OFRA" in line)):
			mrz=line
		result=""
		if ("-1" not in mrz):
			#clean the unnecessary caracters from the extracted str
			result = Fields.clean_alphanum(mrz)
		else:
			result = "-1"
		return self.set_field(result)