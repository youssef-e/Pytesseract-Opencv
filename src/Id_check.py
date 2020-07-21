import json
import os
import sys
import argparse


def get_parent_dir(n=1):
	current_path = os.path.dirname(os.path.abspath(__file__))
	for k in range(n):
		current_path = os.path.dirname(current_path)
	return current_path

utils_path = os.path.join(get_parent_dir(1), "Utils")
sys.path.append(utils_path)

# from Classes.Fields import Fields
# from Classes.Mrz import Mrz
from Classes.Name import Name
from Classes.First_name import First_name
from Classes.Gender import Gender
from Classes.Birthday import Birthday
from Classes.Id_number import Id_number
from Classes.Mrz1 import Mrz1
from Classes.Mrz2 import Mrz2

from Utils import query_yes_no

def distance(str1,str2):
	def cost(x,y):
		return 0 if x==y else 1
	D = [[0 for y in range(len(str2)+1)] for x in range(len(str1)+1)]
	F = [['N' for y in range(len(str2)+1)] for x in range(len(str1)+1)]
	D[0][0] = 0
	F[0][0] = 'N'
	for i in range(1,len(str1)+1):
		D[i][0] = i
		F[i][0] = 'u'
	for j in range(1,len(str2)+1):
		D[0][j] = j
		F[0][j] = 'r'
	for i,c1 in enumerate(str1):
		for j,c2 in enumerate(str2):
			x = D[i][j]+cost(c1,c2)
			y = D[i+1][j]+1
			z = D[i][j+1]+1
			if x <= y and x <= z:
				D[i+1][j+1] = x
				F[i+1][j+1] = 'd'
			elif y <= x and y <= z:
				D[i+1][j+1] = y
				F[i+1][j+1] = 'r'
			else:
				D[i+1][j+1] = z
				F[i+1][j+1] = 'u'
	return (D,F)

def print_alignment(F, i, j,str1,str2):
	ns1 = ''
	ns2 = ''
	while i>0 or j>0:
		if F[i][j] == 'd':
			ns1=str1[i-1]+ns1
			ns2=str2[j-1]+ns2
			i-=1
			j-=1
		elif F[i][j] == 'r':
			ns1=' '+ns1
			ns2=str2[j-1]+ns2
			j-=1
		else:
			ns1=str1[i-1]+ns1
			ns2=' ' +ns2
			i-=1
	return (ns1,ns2)

def get_key(input_string):
	result = 0
	i = -1
	factors = [7, 3, 1]
	for car in input_string:
		if car == "<":
			value = 0
			i += 1
		elif car in "0123456789":
			value = int(car)
			i += 1
		elif car in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			value = ord(car)-55
			i += 1
		else:
			print("Character out of bonds")
			break
		result += value * factors[i%3]
	return result % 10

def data_integrity_check(data):
	if len(data)<7:
		print ("Warning: Missing data in JSon file")
		return False
	try:
		data_object = from_string_to_fields(data)
	except KeyError:
		print("Warning: Missing data in JSon file")
		return False
	else:
		for c in data_object:
			if not data_object[c].synthax_check():
				return False
	return True

#def compare_fields_to_mrz(data):
def compare_to_mrz(data):
	data_object = from_string_to_fields(data)
	name = data_object['Name'].word_to_mrz()
	fname = data_object['First_name'].word_to_mrz()
	id_nbr = data_object['Id_number'].word_to_mrz()
	gender = data_object['Gender'].word_to_mrz()
	birthday = data_object ['Birthday'].word_to_mrz()
	mrz1 = data_object ['Mrz1']
	mrz2 = data_object ['Mrz2']
	mrz_name = mrz1.name_mrz()
	mrz_fname = mrz2.fname_mrz()
	mrz_id_nbr = mrz2.id_nbr_mrz()
	mrz_birthday = mrz2.birthday_mrz()
	mrz_gender = mrz2.gender_mrz()
	mrz_location = mrz1.location_mrz()
	mrz_agent_nbr = mrz1.agent_nbr_mrz()
	print("name differences: ")
	name = compare_strings(mrz_name,name)
	print("first name differences: ")
	fname = compare_strings(mrz_fname,fname)
	print("id number differences: ")
	id_nbr =compare_strings(mrz_id_nbr,id_nbr)
	print("birthday differences: ")
	birthday = compare_strings(mrz_birthday,birthday)
	print("gender differences: ")
	gender = compare_strings(mrz_gender,gender)
	print("location differences: ")
	location = compare_strings(mrz_location,id_nbr[4:7])
	mrz = mrz1.field + mrz2.field
	compared_mrz = "IDFRA"+name+location+mrz_agent_nbr+id_nbr+str(get_key(id_nbr))+fname+birthday+str(get_key(birthday)) + gender
	compared_mrz += str(get_key(compared_mrz))
	print("mrz differences: ")
	print(compare_strings(mrz,compared_mrz))


def compare_strings(mrz_str, str1):
	(D,F) = distance(mrz_str, str1)
	(new_str1,new_str2) = print_alignment(F,len(mrz_str),len(str1),mrz_str,str1)
	arrow =' '*len(new_str1)
	cost = D[len(mrz_str)][len(str1)]
	for i, c in enumerate(new_str1):
		if(new_str2[i]!= c):
			arrow=arrow[:i]+'^'+arrow[i+1:]
	if cost == 1:
		print("mrz:   " + new_str1)
		print("field: " + new_str2)
		print("       " + arrow)
		if query_yes_no("Small difference detected, it may result from the OCR inaccuracy.\n Would you like to replace it ?"):
			index = arrow.index("^")
			new_str2 =  new_str2[:index] + new_str1[index] + new_str2[index+1:]
			arrow=arrow[:index]+' '+arrow[index+1:]
			cost -= 1
	print("mrz:   " + new_str1)
	print("field: " + new_str2)
	print("       " + arrow)
	return new_str2


def from_string_to_fields(data):
	data_object ={}
	dispatcher={'Name':Name,
			'First_name':First_name,
			'Id_number': Id_number,
			'Gender':Gender,
			'Birthday':Birthday,
			'Mrz1':Mrz1,
			'Mrz2':Mrz2
			}
	for c in data:
		data_object[c]=dispatcher[c](data[c])
	return data_object


#--------- Main funtion ------------#


detection_results_folder = os.path.join(get_parent_dir(n=1), "results")
arg = argparse.ArgumentParser()
arg.add_argument(
		"-i","--input",
		type=str,
		default=detection_results_folder,
		help="Output path for detection results. Default is "
		+ detection_results_folder,
		)

FLAGS = arg.parse_args()
result_folder=FLAGS.input
detection_results_file = os.path.join(result_folder, "Detection_Results.json")

with open(detection_results_file) as json_file:
	data = json.load(json_file)

print(str(data) + " len: "+ str(len(data)))
print("data integrity check:")
print(data_integrity_check(data))
compare_to_mrz(data)

