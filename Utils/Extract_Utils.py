from Classes.Fields import Fields
from Classes.Name import Name
from Classes.First_name import First_name
from Classes.Gender import Gender
from Classes.Birthday import Birthday
from Classes.Id_number import Id_number
from Classes.Mrz1 import Mrz1
from Classes.Mrz2 import Mrz2




def fields_extract(extracted_lines):
	fname=First_name("-1")
	birthday = Birthday("-1")
	name = Name("-1")
	gender = Gender("-1")
	id_nbr = Id_number("-1")
	mrz1 = Mrz1("-1")
	mrz2 = Mrz2("-1")
	for i, extracted_line in enumerate(extracted_lines):
		line = extracted_line
		if ((" Nom" in line ) or (" Mom" in line) or (" nom" in line) or (" Non " in line) or (" non" in line) or ("Now" in line)):
			if not is_found(name):
				name.extract(line)
	  
		elif (("Pren" in line) or ("preno" in line) or ("Prenom" in line) or ("Pre" in line)):
			if not is_found(fname):
				fname.extract(line)
			try:
				line=extracted_lines[i+1]
			except IndexError:
				birthday.set_field("-1")
				gender.set_field("-1")
			else:
				if not is_found(birthday):
					birthday.extract(line)
				if not is_found(gender):
					gender.extract(line)
			
		elif (("ationale" in line.lower()) or ("carte" in line.lower()) or (" identite" in line.lower())):
			if not is_found(name):
				id_nbr.extract(line)
			try:
				line=extracted_lines[i+1]
			except IndexError:
				name.set_field("-1")
			else:
				if not is_found(name):
					name.extract(line)
		else:
			line=Fields.clean_alphanum(line).upper()
			if("<<" in line and ("IDFRA" in line or "IOFRA" in line or "DFRA" in line or "OFRA" in line)):
				if not is_found(mrz1):	
					mrz1.extract(line)
				try:
					line=extracted_lines[i+1]
				except IndexError:
					mrz2.set_field("-1")
					print("mrz2 not found")
				else:
					if not is_found(mrz2):	
						mrz2.extract(line)
	result = {
	"name" : str(name),
	"fname" : str(fname),
	"id_nbr" : str(id_nbr),
	"gender" : str(gender),
	"birthday" : str(birthday),
	"mrz1" : str(mrz1),
	"mrz2" : str(mrz2)
	}

	for i,(k,v) in enumerate(result.items()):
		result[k]="-1" if v == "" else result[k]
	return result




def is_found(string):
	if("-1" in string):
		return False
	return True

