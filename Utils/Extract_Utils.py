from Classes.Fields import Fields
from Classes.Mrz import Mrz
from Classes.Name import Name
from Classes.First_name import First_name
from Classes.Gender import Gender
from Classes.Birthday import Birthday
from Classes.Id_number import Id_number
from Classes.Mrz1 import Mrz1
from Classes.Mrz2 import Mrz2
import json
import unicodedata
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/Users/youssef/Application/Homebrew/Cellar/tesseract/4.1.1/bin/tesseract'

from Image_Process_Utils import apply_threshold

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
	"name" : name,
	"fname" : fname,
	"id_nbr" : id_nbr,
	"gender" : gender,
	"birthday" : birthday,
	"mrz1" : mrz1,
	"mrz2" : mrz2
	}

	for i,(k,v) in enumerate(result.items()):
		result[k]="-1" if v == "" else result[k]
	return result

def is_found(string):
	if("-1" in string):
		return False
	return True

#clean the text from empty lines
def clean_result(text,char):
    lines=text.split(char)
    return [line for line in lines if line.strip() != ""]

def get_Strings(image, gray, scores1,scores2):
    names = []
    fnames = []
    id_nbrs = []
    genders = []
    birthdays= []
    mrz1s=[]
    mrz2s=[]
    for i in range(1,21):
        thresh = apply_threshold(image,gray,i)
        result = pytesseract.image_to_string(thresh, lang='fra')
        result= unicodedata.normalize("NFKD",result).encode('ascii', 'ignore').decode('ascii')
        print('#=======================================================')
        print("#=================== filter "+str(i)+" ===================")
        print('#=======================================================')
        #print(result)
        lines= clean_result(result, '\n')
        for line in lines:
            print(line)
            print("~~~~~~")
        idcard = fields_extract(lines)
        names.append(idcard["name"])
        fnames.append(idcard["fname"])
        id_nbrs.append(idcard["id_nbr"])
        genders.append(idcard["gender"])
        birthdays.append(idcard["birthday"])
        mrz1s.append(idcard["mrz1"])
        mrz2s.append(idcard["mrz2"])
        #cv2.imshow('img'+str(i), thresh)
    
    #result = unicodedata.normalize("NFKD",pytesseract.image_to_string(image, lang='fra')).encode('ascii', 'ignore').decode("utf-8")
    print('#=======================================================')
    print('#==================== extracted data ===================')
    print('#=======================================================')
    print("~~~~~~~~ names ~~~~~~~")
    for i, name in enumerate(names,1):
        print(str(i)+": "+str(name)+" len: "+ str(len(name)))
    print("~~~~~~~~ fnames ~~~~~~~")
    for i, fname in enumerate(fnames,1):
        print(str(i)+": "+str(fname)+" len: "+ str(len(fname)))
    print("~~~~~~~~ id nbrs ~~~~~~~")
    for i, id_nbr in enumerate(id_nbrs,1):
        print(str(i)+": "+str(id_nbr)+" len: "+ str(len(id_nbr)))
    print("~~~~~~~~ gender ~~~~~~~")
    for i, gender in enumerate(genders,1):
        print(str(i)+": "+str(gender)+" len: "+str(len(genders)))
    print("~~~~~~~~ birthday ~~~~~~~")
    for i, birthday in enumerate(birthdays,1):
        print(str(i)+": "+str(birthday)+" len: "+str(len(birthday)))
    print("~~~~~~~~ mrz 1 ~~~~~~~")
    for i, mrz1 in enumerate(mrz1s,1):
        print(str(i)+": "+str(mrz1)+" len: "+str(len(mrz1)))
    print("~~~~~~~~ mrz 2 ~~~~~~~")
    for i, mrz2 in enumerate(mrz2s,1):
        print(str(i)+": "+str(mrz2)+" len: "+str(len(mrz2)))
   
    x = {
    "Name" : Fields.mean_word(names,scores1),
    "First_name" : Fields.mean_word(fnames,scores1),
    "Id_number" : Fields.mean_word(id_nbrs,scores1),
    "Gender" : Fields.mean_word(genders,scores1),
    "Birthday" : Fields.mean_word(birthdays,scores1),
    "Mrz1" : Mrz.mean_word(mrz1s,scores2),
    "Mrz2" : Mrz.mean_word(mrz2s,scores2)
    }
    y=json.dumps(x,sort_keys=True,indent=4)
    print(y)
    return x