import json
import os
import sys
import argparse


def get_parent_dir(n=1):
	""" returns the n-th parent dicrectory of the current working directory."""

	current_path = os.path.dirname(os.path.abspath(__file__))
	for k in range(n):
		current_path = os.path.dirname(current_path)
	return current_path

utils_path = os.path.join(get_parent_dir(1), "Utils")
sys.path.append(utils_path)

from Classes.Fields import Fields
from Classes.Mrz import Mrz
from Classes.Name import Name
from Classes.First_name import First_name
from Classes.Gender import Gender
from Classes.Birthday import Birthday
from Classes.Id_number import Id_number
from Classes.Mrz1 import Mrz1
from Classes.Mrz2 import Mrz2



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
		data = from_string_to_fields(data)
		print(data)
	except KeyError:
		print("Warning: Missing data in JSon file")
		return False
	else:
		for c in data:
			if not data[c].synthax_check():
				return False
	return True

def compare_fields_to_mrz(data):
    

def from_string_to_fields(data):
	dispatcher={'Name':Name,
			'First_name':First_name,
			'Id_number': Id_number,
			'Gender':Gender,
			'Birthday':Birthday,
			'Mrz1':Mrz1,
			'Mrz2':Mrz2
			}
	for c in data:
		data[c]=dispatcher[c](data[c])
	return data


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
# print(get_key(data['Id_number']))
# print(birthday_to_MRZ(data['Birthday']))
# print(get_key(birthday_to_MRZ(data['Birthday'])))

