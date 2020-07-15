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

	for i in range(len(str1)):
		for j in range(len(str2)):
			x = D[i][j]+cost(str1[i],str2[j])
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
	print(name)
	fname = data_object['First_name'].word_to_mrz()
	id_nbr = data_object['Id_number'].word_to_mrz()
	gender = data_object['Gender'].word_to_mrz()
	birthday = data_object ['Birthday'].word_to_mrz()
	mrz1 = data_object ['Mrz1'].word_to_mrz()
	mrz2 = data_object ['Mrz2'].word_to_mrz()
	mrz_name = mrz1[5:30]
	mrz_fname = mrz2[13:27]
	mrz_id_nbr = mrz2[:12]
	mrz_birthday = mrz2[27:33]
	mrz_gender = mrz2[34]
	mrz_location = mrz1[30:33]
	print("name differences: ")
	print(compare_strings(mrz_name,name))
	print("first name differences: ")
	print(compare_strings(mrz_fname,fname))
	print("id number differences: ")
	print(compare_strings(mrz_id_nbr,id_nbr))
	print("birthday differences: ")
	print(compare_strings(mrz_birthday,birthday))
	print("gender differences: ")
	print(compare_strings(mrz_gender,gender))
	print("location differences: ")
	print(compare_strings(mrz_location,id_nbr[4:7]))


def compare_strings(mrz_str, str1):
	(D,F)=distance(mrz_str, str1)
	(new_str1,new_str2)=print_alignment(F,len(mrz_str),len(str1),mrz_str,str1)
	arrow =' '*len(new_str1)
	cost = D[len(mrz_str)][len(str1)]
	for i in range(len(new_str1)):
		if(new_str2[i]!=new_str1[i]):
			arrow=arrow[:i]+'^'+arrow[i+1:]
			print(new_str1)
			print(arrow)
			print(new_str2)
			print(arrow)
	return cost


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
# print(get_key(data['Id_number']))
# print(birthday_to_MRZ(data['Birthday']))
# print(get_key(birthday_to_MRZ(data['Birthday'])))
