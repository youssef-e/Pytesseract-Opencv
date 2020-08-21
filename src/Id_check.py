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
from Classes.Fields import Fields

from Utils import query_yes_no

detection_results_folder = os.path.join(get_parent_dir(n=1), "results")
# arg = argparse.ArgumentParser()
# arg.add_argument(
# 		"-i","--input",
# 		type=str,
# 		default=detection_results_folder,
# 		help="Output path for detection results. Default is "
# 		+ detection_results_folder,
# 		)
# FLAGS = arg.parse_args()
result_folder=detection_results_folder
detection_results_file = os.path.join(result_folder, "Detection_Results.json")
id_check_results_file = os.path.join(result_folder, "Id_check_Results.json")

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
			ns1=ns1
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
				print("error found in",c)
				return False
	return True

#def compare_fields_to_mrz(data):
def compare_to_mrz(data):
	#converting fields to mrz
	data_object = from_string_to_fields(data)
	name = data_object['Name'].word_to_mrz()
	fname = data_object['First_name'].word_to_mrz()
	id_nbr = data_object['Id_number'].word_to_mrz()
	gender = data_object['Gender'].word_to_mrz()
	if data_object ['Birthday'].synthax_check():
		birthday = data_object ['Birthday'].word_to_mrz()
	else:
		birthday = data_object ['Birthday']
	mrz1 = data_object ['Mrz1']
	mrz2 = data_object ['Mrz2']
	if mrz1.synthax_check()[0] and mrz2.synthax_check()[0] :
		#extracting relevant data from mrz
		mrz_name = mrz1.name_mrz()
		mrz_fname = mrz2.fname_mrz()
		mrz_id_nbr = mrz2.id_nbr_mrz()
		mrz_birthday = mrz2.birthday_mrz()
		mrz_gender = mrz2.gender_mrz()
		mrz_location = mrz1.location_mrz()
		mrz_agent_nbr = mrz1.agent_nbr_mrz()
		#comparing the fields with their corresponding mrz data
		print("name differences: ")
		(name, name_diff )= compare_strings(mrz_name,name, 'Name')
		print("first name differences: ")
		(fname,fname_diff) = compare_strings(mrz_fname,fname,'First_name')
		print("id number differences: ")
		(id_nbr, id_nbr_diff) =compare_strings(mrz_id_nbr,id_nbr,'Id_number')
		print("birthday differences: ")
		(birthday, birthday_diff) = compare_strings(mrz_birthday,birthday,'Birthday')
		print("gender differences: ")
		(gender,gender_diff) = compare_strings(mrz_gender,gender,'Gender', False)
		print("location differences: ")
		(location,location_diff) = compare_strings(mrz_location,id_nbr[4:7],'Field')
		#comparing the extracted mrz with the reconstructed one (including the control keys)
		mrz = mrz1.field + mrz2.field
		compared_mrz = "IDFRA"+name+location+mrz_agent_nbr+id_nbr+str(get_key(id_nbr))+fname+birthday+str(get_key(birthday)) + gender
		compared_mrz1 = "IDFRA"+name+location+mrz_agent_nbr
		compared_mrz2 =  id_nbr+str(get_key(id_nbr))+fname+birthday+str(get_key(birthday)) + gender + str(get_key(compared_mrz))
		compared_mrz += str(get_key(compared_mrz))
		print("mrz differences: ")
		(mrz, mrz_diff)= compare_strings(mrz,compared_mrz,'MRZ',False)
		(mrz1, mrz1_diff)= compare_strings(mrz1.field,compared_mrz1,'MRZ',False)
		(mr2, mrz2_diff)= compare_strings(mrz2.field,compared_mrz2,'MRZ',False)
		new_data = {
			'Name': name_diff,
			'First_name': fname_diff,
			'Id_number': id_nbr_diff,
			'Birthday': birthday_diff,
			'Gender': gender_diff,
			'Mrz1': mrz1_diff,
			'Mrz2': mrz2_diff
			}
	else:
		new_data = {
			"error":"mrz is incorrect"
		}
	print(json.dumps(new_data,sort_keys=False,indent=4))
	return new_data

def compare_strings(mrz_str, str1, obj_type, correct=True):
	(D,F) = distance(mrz_str, str1)
	(mrz,new_str) = print_alignment(F,len(mrz_str),len(str1),mrz_str,str1)
	arrow =' '*len(mrz)
	cost = 0
	if (len(new_str)-len(mrz)==1):	
		new_str=new_str[:len(new_str)-1]
	for i, c in enumerate(mrz):
		if(new_str[i]!= c):
			arrow=arrow[:i]+'^'+arrow[i+1:]
			cost+=1
	initial_cost = cost
	if cost < 2 and correct:
		if len(str1)<3 and cost>0:
			cost=1
		while cost > 0:
			print("mrz:   " + mrz)
			print("field: " + new_str)
			print("       " + arrow)
			index = arrow.find("^")
			new_str =  new_str[:index] + mrz[index] + new_str[index+1:]
			cost -= 1
	print("mrz:   " + mrz)
	print("field: " + new_str)
	print("       " + arrow)
	if obj_type == 'MRZ':
		field = {
		"original" : mrz_str,
		"modified" : new_str,
		"cost" : initial_cost
	}
	else:
		field = {
		"original" : from_string_to_field(mrz_str,obj_type).mrz_to_word(),
		"modified" : from_string_to_field(new_str,obj_type).mrz_to_word(),
		"cost" : initial_cost
	}
	return (new_str,field)


def from_string_to_fields(data):
	data_object ={}
	dispatcher={
		'Name':Name,
		'First_name':First_name,
		'Id_number': Id_number,
		'Gender':Gender,
		'Birthday':Birthday,
		'Mrz1':Mrz1,
		'Mrz2':Mrz2,
		'Field':Fields
		}
	for c in data:
		data_object[c]=dispatcher[c](data[c])
	return data_object

def from_string_to_field(string, type):
	dispatcher={
		'Name':Name,
		'First_name':First_name,
		'Id_number': Id_number,
		'Gender':Gender,
		'Birthday':Birthday,
		'Mrz1':Mrz1,
		'Mrz2':Mrz2,
		'Field':Fields
		}
	result=dispatcher[type](string)
	return result

def check(task_id):
	detection_results_file = os.path.join(result_folder, "Detection_Results{}.json".format(task_id))
	id_check_results_file = os.path.join(result_folder, "Id_check_Results{}.json".format(task_id))
	with open(detection_results_file) as json_file:
		data = json.load(json_file)

	print(str(data) + " len: "+ str(len(data)))
	print("data integrity check:")
	print(data_integrity_check(data))
	new_data = compare_to_mrz(data)
	with open(id_check_results_file, 'w') as f:
		json.dump(new_data, f,sort_keys=False,indent=4)

#--------- Main funtion ------------#
	if __name__ == "__main__":
		check()

