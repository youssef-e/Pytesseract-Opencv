import json
import os
import sys
import argparse




def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


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
        birthday = data['Birthday']
        fname = data['First_name']
        gender = data['Gender']
        id_nbr = data['Id_number']
        name = data['Name']
        mrz1 = data['MRZ_l1']
        mrz2 = data['MRZ_l2']
    except KeyError:
        print("Warning: Missing data in JSon file")
        return False
    else:

        if len(birthday) != 10 or birthday == "-1":
            print("Warning: Incorrect Birthday data")
            return False
        if len(fname) < 2 or fname == "-1":
            print("Warning: Incorrect First_name data")
            return False
        if len(name) < 2 or name == "-1":
            print("Warning: Incorrect Name data")
            return False
        if len(gender) != 1 or gender == "-1":
            print("Warning: Incorrect Gender data")
            return False
        if len(id_nbr) != 12 or id_nbr == "-1":
            print("Warning: Incorrect Id_number data")
            return False
        if len(mrz1) != 36 or mrz1 == "-1":
            print("Warning: Incorrect MRZ_l1 data")
            return False
        if len(mrz2) != 36 or mrz2 == "-1":
            print("Warning: Incorrect MRZ_l2 data")
            return False
    return True

def birthday_to_MRZ (birthday):
    date = birthday.split(" ")
    return date[2][2:]+date[1]+date[0]


def name_to_mrZ(name):
    result = ""
    for c in name:
        if()







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
print(get_key(data['Id_number']))
print(birthday_to_MRZ(data['Birthday']))
print(get_key(birthday_to_MRZ(data['Birthday'])))