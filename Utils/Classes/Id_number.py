from Classes.Fields import Fields

class Id_number(Fields):

	#look for the id in the extracted lines using key words to locate it; it returns a str
	def extract(self, line):
		id_nbr="-1"
		if ("ationale" in line.lower() or "carte" in line.lower() or " identite" in line.lower()):
			id_nbrs = line.split(" ")
			for value in id_nbrs:
				notFound = True
				for c in value:
					if notFound :
						if(c>='0' and c<='9'):
							id_nbr=value
							notFound = False
							break
						else:
							break
		return self.set_field(id_nbr)

	def synthax_check(self):
		if len(self) != 12 or self.field == "-1":
			print("Warning: Incorrect data")
			return False
		return True