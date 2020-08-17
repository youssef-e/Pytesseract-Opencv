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
			while len(result)>36:
				index = result.find('<',20)
				if index != -1:
					result = result[:index] + result[index+1:]
				else:
					break
		else:
			result = "-1"
		return self.set_field(result)

	def name_mrz(self):
		return self.field[5:30]
	def location_mrz(self):
		return self.field[30:33]
	def agent_nbr_mrz(self):
		return self.field[33:]

	def synthax_check(self):
		if len(self) != 36 or self.field == "-1":
			error="Warning: Incorrect lenght : MRZ1"
			print(error)
			return (False,error)
		return (True,"")