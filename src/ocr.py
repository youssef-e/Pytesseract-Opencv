# import the necessary packages
import unicodedata
from PIL import Image, ImageChops
import pytesseract
import argparse
from cv2 import *
import os
import numpy as np
import re
import time
import math
import json
import fitz
pytesseract.pytesseract.tesseract_cmd = r'/Users/youssef/Application/Homebrew/Cellar/tesseract/4.1.1/bin/tesseract'




def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im

def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

# Rescale the image, if needed.
def rescaling(image, imagename):
    im_pil=img_pil = Image.fromarray(image)
    imagepaths=imagename.split("/")
    imagenames=imagepaths[len(imagepaths)-1].split(".")

    imagename=detection_results_folder+"/"+imagenames[len(imagenames)-2]+"600dpi."+imagenames[len(imagenames)-1]  
    print(imagename)
    img_pil = img_pil.save(imagename, dpi=(600, 600))
    image = cv2.imread(imagename)
    print(image.shape)
    d=(1024,768)
    if image.shape[0] > image.shape[1]:
        image=deskew(image)
    if image.shape[0] == image.shape[1]:
        scale_percent = int(900 * 100 /image.shape[0]) # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        d = (width, height)
    img = cv2.resize(image, d, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    print(img.shape)
    os.remove(imagename)
    return img

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
	# Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(image, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (5, 5), 0)
    return img
 
#thresholding with different filters
def apply_threshold(img,gray, argument):
    kernel = np.ones((1,1), np.uint8)
    switcher = {
        1: cv2.erode(cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],kernel,iterations=1),
        2: cv2.erode(cv2.threshold(cv2.GaussianBlur(img, (3, 3), 0), 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],kernel,iterations=1),
        3: cv2.erode(cv2.threshold(cv2.GaussianBlur(img, (1, 1), 0), 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],kernel,iterations=1),
        4: cv2.threshold(cv2.GaussianBlur(img, (3, 3), 0), 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        5: cv2.threshold(cv2.GaussianBlur(img, (1, 1), 0), 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        6: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        7: cv2.threshold(cv2.medianBlur(img, 5), 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        8: cv2.threshold(cv2.medianBlur(img, 3), 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        9: cv2.threshold(cv2.medianBlur(img, 1), 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        10: cv2.adaptiveThreshold(cv2.bilateralFilter(img,9,40,100), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2),
        11: cv2.threshold(cv2.bilateralFilter(img,3,75,75),127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        12: img,
        13: gray,
        14: cv2.adaptiveThreshold(cv2.bilateralFilter(gray,7,75,75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2),
        15: cv2.adaptiveThreshold(cv2.bilateralFilter(gray,8,75,75), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2),
        16: cv2.adaptiveThreshold(cv2.bilateralFilter(gray,7,75,75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 2),
        17: cv2.adaptiveThreshold(cv2.bilateralFilter(gray,3,75,75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2),
        18: cv2.adaptiveThreshold(cv2.bilateralFilter(img,8,75,75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2),
        19: cv2.morphologyEx(cv2.adaptiveThreshold(cv2.bilateralFilter(img,8,75,75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2),cv2.MORPH_CLOSE, kernel),
        20: cv2.threshold(img,127,255,cv2.THRESH_TOZERO)[1]


    }
    return switcher.get(argument, "Invalid method")

#deskew 
def deskew(image):
   
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    
    #This second bit detect smaller inclination angle and correct it

    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle
    # rotate the image to deskew it
    print("[ANGLE] "+str(angle))
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    image = cv2.warpAffine(image, M, (w, h),
       flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    try:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
        lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
        angles = []

        for x1, y1, x2, y2 in lines[0]:
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)

            median_angle = np.median(angles)
            print("[ANGLE 2] "+str(median_angle))
            img_pil = Image.fromarray(image)
            img_pil = img_pil.rotate(median_angle, expand=True)
        #convert the pil image to cv2 image
        image = np.asarray(img_pil)
    except TypeError:
        print("image too small to deskew")    
    #this bit detect if the image is upside down or at 90 or 270 degree
    #then rotate it
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        #use tesseract image_to_osd method to detect angles of rotation
        rot_data = pytesseract.image_to_osd(image, lang='fra')
    except pytesseract.pytesseract.TesseractError:
        print("Too few characters/resolution in image to osd")
    else:
        print("[OSD] "+rot_data)
        rot = re.search('(?<=Rotate: )\d+', rot_data).group(0)
        #calculation of the correction angle
        angle = float(rot)
        if angle > 0:
            angle = 360 - angle
        print("[ANGLE 3] "+str(angle))
        # rotate the image to deskew it
        img_pil = Image.fromarray(image)
        img_pil = img_pil.rotate(angle, expand=True)
        #convert the pil image to cv2 image
        image = np.asarray(img_pil)
    
    finally:
        return image

#clean the text from empty lines
def clean_result(text,char):
	lines=text.split(char)
	return [line for line in lines if line.strip() != ""]


def get_Strings(image, gray):
    names = []
    fnames = []
    id_nbrs = []
    nationalities = []
    genders = []
    birthdays= []
    mrz1s=[]
    mrz2s=[]
    for i in range(1,21):
        thresh = apply_threshold(img,gray,i)
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
        names.append(name_extract(lines))
        fnames.append(first_name_extract(lines))
        id_nbrs.append(id_extract(lines))
        nationalities.append(nationality_extract(lines))
        genders.append(gender_extract(lines))
        birthdays.append(birthday_extract(lines))
        mrz1s.append(mrz1_extract(lines))
        mrz2s.append(mrz2_extract(lines))
        cv2.imshow('img'+str(i), thresh)
    
    """ image = apply_threshold(img,6)
    result = unicodedata.normalize("NFKD",pytesseract.image_to_string(image, lang='fra')).encode('ascii', 'ignore').decode("utf-8")
    lines= clean_result(result)
    for line in lines:
        print(line)
        print("~~~~~~")
    names.append(name_extract(lines))
    fnames.append(first_name_extract(lines))
        #if(i==1)
    cv2.imshow('img',image)"""
    print('#=======================================================')
    print('#==================== extracted data ===================')
    print('#=======================================================')
    print("~~~~~~~~ names ~~~~~~~")
    for i, name in enumerate(names,1):
        print(str(i)+": "+name+" len: "+ str(len(name)))
    print("~~~~~~~~ fnames ~~~~~~~")
    for i, fname in enumerate(fnames,1):
        print(str(i)+": "+fname+" len: "+ str(len(fname)))
    print("~~~~~~~~ id nbrs ~~~~~~~")
    for i, id_nbr in enumerate(id_nbrs,1):
        print(str(i)+": "+id_nbr+" len: "+ str(len(id_nbr)))
    print("~~~~~~~~ nationality ~~~~~~~")
    for i, nationality in enumerate(nationalities,1):
        print(str(i)+": "+nationality+" len: "+str(len(nationality)))
    print("~~~~~~~~ gender ~~~~~~~")
    for i, gender in enumerate(genders,1):
        print(str(i)+": "+gender+" len: "+str(len(genders)))
    print("~~~~~~~~ birthday ~~~~~~~")
    for i, birthday in enumerate(birthdays,1):
        print(str(i)+": "+birthday+" len: "+str(len(birthday)))
    print("~~~~~~~~ mrz 1 ~~~~~~~")
    for i, mrz1 in enumerate(mrz1s,1):
        print(str(i)+": "+mrz1+" len: "+str(len(mrz1)))
    print("~~~~~~~~ mrz 2 ~~~~~~~")
    for i, mrz2 in enumerate(mrz2s,1):
        print(str(i)+": "+mrz2+" len: "+str(len(mrz2)))
    
    x = {
    "Name" : mean_word(names),
    "First_name" : mean_word(fnames),
    "Id_number" : mean_word(id_nbrs),
    "Nationality" : mean_word(nationalities),
    "Gender" : mean_word(genders),
    "Birthday" : mean_word(birthdays),
    "MRZ_l1" : mean_mrz(mrz1s),
    "MRZ_l2" : mean_mrz(mrz2s)
    }
    y=json.dumps(x,sort_keys=True,indent=4)
    print(y)
    return x

#look for the name in the extracted lines using key words to locate it; it returns a str
def name_extract(extracted_lines):
    name="-1"
    for i in range(len(extracted_lines)):
        line=extracted_lines[i]
        if ((" Nom" in line ) or (" Mom" in line) or (" nom" in line) or (" Non " in line) or (" non" in line)):
            cleanedLine=line
            for c in line:
                    if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '-') and(c !=" ") and(c!= ":")):
                        cleanedLine=cleanedLine.replace(c,"")
            words = cleanedLine.split(":")[len(cleanedLine.split(":"))-1].split(" ")
            k=1
            while(k<=len(words)-1):
                if(len(words[len(words)-k])>2):
                    name=words[len(words)-k]
                k = k + 1
            break
        elif (("Pren" in line) or ("preno" in line) or ("Prenom" in line) or ("Pre" in line)):
            line=extracted_lines[i-1]
            cleanedLine=line
            for c in line:
                    if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '-') and(c !=" ") and(c!= ":")):
                        cleanedLine=cleanedLine.replace(c,"")
            words = cleanedLine.split(":")[len(cleanedLine.split(":"))-1].split(" ")
            k=1
            while(k<=len(words)-1):
                if(len(words[len(words)-k])>2):
                    name=words[len(words)-k]
                k = k + 1
            break
        elif (("ationale" in line.lower()) or ("carte" in line.lower()) or (" identite" in line.lower())):
            try:
                line=extracted_lines[i+1]
            except IndexError:
                name ="-1"
            else:
                cleanedLine=line
                for c in line:
                    if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '-') and(c !=" ") and(c!= ":")):
                        cleanedLine=cleanedLine.replace(c,"")
                words = cleanedLine.split(":")[len(cleanedLine.split(":"))-1].split(" ")
                k=1
                while(k<=len(words)-1):
                    if(len(words[len(words)-k])>2):
                        name=words[len(words)-k]
                    k = k + 1
                break
    if(name==""):
        name = "-1"
    return name

#look for the first name(s) in the extracted lines using key words to locate it/them; it returns a str containing the first names separated with spaces
def first_name_extract(extracted_lines):
    name="-1"
    for line in extracted_lines:
        if ("Pren" in line or "preno" in line or "Prenom" in line or "Pre" in line):
            name = line.split(":")[len(line.split(":"))-1]
            break
    names= name.split(" ")
    fname= ""
    l = len(names)
    j = 0
    while(j<l):
        word=names[j]
        #cleaning unnecessary words and spaces from the line
        if("Pren" in word or "preno" in word or "Prenom" in word or "Pre" in word):
            names[j]=""
        if(names[j]==""):
            names.pop(j)
            j=j-1
            l=l-1
        else:
            if ("-1" not in names[j]):
                #clean the unnecessary caracters from the extracted name(s)
                for i in range(len(names[j])):
                    if ((names[j][i]<'a'or names[j][i]>'z') and (names[j][i]<'A'or names[j][i]>'Z') and (names[j][i] != '-')):
                        word=word.replace(names[j][i],"")
                if word != "":
                    fname = fname + word + " "
            else:
                fname = "-1"
        j=j+1
    if fname =="":
        fname = "-1"
    if (fname !="-1"):
        if(fname[0]==" "):    
            fname=fname.replace(fname[0],"")
        l=len(fname)
        i=l-1
        while(i<l):
            if((fname[i]<'a' or fname[i]>'z') and (fname[i]<'A' or fname[i]>'Z')):
                fname=fname[:i]
                l=len(fname)
                i=l-1
            else:
                break
    return fname

#look for the id in the extracted lines using key words to locate it; it returns a str
def id_extract(extracted_lines):
    id_nbr="-1"
    for line in extracted_lines:
        if ("ationale" in line.lower() or "carte" in line.lower() or " identite" in line.lower()):
            id_nbrs = line.split(" ")
            for value in id_nbrs:
                for c in value:
                    if(c>='0' and c<='9'):
                        id_nbr=value                   
                        break
                    else:
                        break
            break

    return id_nbr

#look for the nationality in the extracted lines using key words to locate it; it returns a str
def nationality_extract(extracted_lines):
    nationality="-1"
    for line in extracted_lines:
        if ("Natio" in line or "alite" in line or " ation" in line or "onatite" in line):
            nationality = line.split(" ")[len(line.split(" "))-1]

            break

    return nationality

#look for the birthday in the extracted lines using key words to locate it; it returns a str
def birthday_extract(extracted_lines):
    result="-1"
    for i in range(len(extracted_lines)):
        line = extracted_lines[i]
        #since the line containing the birthday tend to not be read correctly
        #it first look for the line containing the first name, then try
        #to locate the birthday in the line below it
        if ("Pren" in line or "preno" in line or "Prenom" in line or "Pre" in line):
            try:
                words = extracted_lines[i+1].replace("."," ").split(" ")
            except IndexError:
                print("Ocr not accurate enough")
            else:
                clean_line=[]
                #the extracted line then need to be cleaned of non alphanumerical caractere to normilize the date format
                for word in words:
                    clean_word=word
                    for c in word:
                        if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c <'0' or c>'9')):
                            clean_word = clean_word.replace(c," ")
                    w = word.split(" ")
                    for value in w:
                        if value !="":
                            clean_line.append(value)
                #it then can extract the date        
                try:
                    result = clean_line[len(clean_line)-3]+" "+clean_line[len(clean_line)-2]+" "+clean_line[len(clean_line)-1]
                except IndexError:
                    result="-1"
                    break
                else:
                    for c in result:
                        if((c <'0' or c>'9') and (c!=" ")):
                            result="-1"
                            break
                break
            #however if the image is too small, they may not be any lines below the firstname, it then sends an error       
    return result

#look for the gender in the extracted lines using key words to locate it; it returns a str
def gender_extract(extracted_lines):
    gender = "-1"
    for i in range(len(extracted_lines)):
        line = extracted_lines[i]
        #since the line containing the gender tend to not be read correctly
        #it first look for the line containing the first name, then try
        #to locate the gender in the line below it
        if ("Pren" in line or "preno" in line or "Prenom" in line or "Pre" in line):
            try:
                words = extracted_lines[i+1].replace("."," ").split(" ")
                for word in words:
                    if(word == "M" or word =="F"):
                        gender = word
                        break
            #however if the image is too small, they may not be any lines below the firstname, it then sends an error
            except IndexError:
                print("Ocr not accurate enough")
    return gender    
#look for the mrz in the extracted lines using key words to locate it; it returns a list of str
def mrz1_extract(extracted_lines):
    mrz="-1"
    for line in extracted_lines:
        line = line.upper()
        if("<<" in line and ("IDFRA" in line or "IOFRA" in line or "DFRA" in line or "OFRA" in line)):
            mrz=line
            break
    result=""
    word=mrz
    if ("-1" not in mrz):
        #clean the unnecessary caracters from the extracted str
        for c in mrz:
            if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '<') and (c <'0' or c >'9')):
                word=word.replace(c,"")
        result = result + word
    else:
        result = "-1"
    return result

def mrz2_extract(extracted_lines):
    mrz="-1"  
    for j in range(len(extracted_lines)):
        line = extracted_lines[j].upper()
        word=line
        n_line=""
        for c in line:
            if ((c <'a'or c >'z') and ( c <'A'or c >'Z') and (c != '<') and (c <'0' or c >'9')):
                word=word.replace(c,"")
        n_line = n_line + word
        if("<<" in n_line and ("IDFRA" in n_line or "IOFRA" in n_line or "DFRA" in n_line or "OFRA" in n_line)):
            try:
                mrz=extracted_lines[j+1]
                break
            except IndexError:
                print("indexerror")
                break
    result=""
    word=mrz
    if ("-1" not in mrz):
        #clean the unnecessary caracters from the extracted str
        for c in mrz:
            if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '<') and (c <'0' or c >'9')):
                word=word.replace(c,"")
        result = result + word
    else:
        result = "-1"
    return result
            

def mean_length(words):
    mean_lengths=[]
    max_occur=0
    mean_length=0
    for word in words:
        if word != "-1":
            mean_lengths.append(len(word))
    for length in mean_lengths:
        if(max_occur<mean_lengths.count(length)):
            max_occur=mean_lengths.count(length)
            mean_length = length
        if(isinstance(mean_length,str)):
            mean_length = 0
    return mean_length 

def mean_length_mrz(words):
    mean_lengths=[]
    max_occur=0
    mean_length=0
    for word in words:
        if word != "-1":
            mean_lengths.append(len(word))
    for length in mean_lengths:
        if(length == 36):
            return  length
        if(max_occur<mean_lengths.count(length)):
            max_occur=mean_lengths.count(length)
            mean_length = length
        if(isinstance(mean_length,str)):
            mean_length = 0
    return mean_length  

def mean_word(words):
    mean_len = mean_length(words)
    final_word = ""
    for i in range(mean_len):
        chars={}        
        for word in words:
            if len(word) == mean_len:
                if word[i] in chars:
                    if(len(words)>11 and (words[11]==word or words[12]==word or words[14]==word)):
                        chars[word[i]] =chars[word[i]] + 3
                    else:
                        chars[word[i]] =chars[word[i]] + 0.5
                else:
                    if(len(words)>11 and (words[11]==word or words[12]==word or words[14]==word)):
                        chars[word[i]] = 3
                    else:
                        chars[word[i]] = 0.5
        max_val=-1
        key=""
        for c in chars:
            if chars[c]>=max_val:
                max_val=chars[c]
                key = c
        final_word = final_word + key 
    return final_word

def mean_mrz(words):
    mean_len = mean_length_mrz(words)
    final_word = ""
    for i in range(mean_len):
        chars={}        
        for word in words:
            if len(word) == mean_len:
                if word[i] in chars:
                    if(len(words)>16 and (words[17]==word)):
                        chars[word[i]] =chars[word[i]] + 3
                    else:
                        chars[word[i]] = chars[word[i]] + 1
                else:
                    if(len(words)>16 and (words[17]==word)):
                        chars[word[i]] = 3
                    else:
                        chars[word[i]] = 1
        max_val=-1
        key=""
        for c in chars:
            if c == "<" or c=="(" or c == "[" or c == "{":
                key = "<"
                break
            elif ((c == "S" or c == "C") and ( i-1 >= 0 and len(final_word) !=0) and (final_word[i-1] == "<")):
                key = "<"
                break
            elif chars[c]>=max_val:
                max_val=chars[c]
                key = c
        final_word = final_word + key 
    return final_word



#~~~~~~~~~~~~~~ Main function ~~~~~~~~~~~~~~~~~#
#variable declaration
detection_results_folder = os.path.join(get_parent_dir(n=1), "results")


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-i", "--image",
    required=True,
    help="path to input image to be OCR'd"
)

ap.add_argument(
        "-njs", "--no_js",
        default=False,
        action="store_true",
        help="save the output in a JSON file. Default is False.",
    )

ap.add_argument(
        "-o","--output",
        type=str,
        default=detection_results_folder,
        help="Output path for detection results. Default is "
        + detection_results_folder,
    )
FLAGS = ap.parse_args()

#declaration of variables
save_result= not FLAGS.no_js
result_folder=FLAGS.output
input_file = FLAGS.image
delete = False

#detect if the input file is a pdf, and if it is, covert it to png
if(input_file.split(".")[len(input_file.split("."))-1]=="pdf"):
    doc = fitz.open(input_file)
    page = doc.loadPage(0) #number of page
    pix = page.getPixmap()
    input_file = detection_results_folder+"/pdfToimage.png"
    pix.writePNG(input_file)
    delete = True
#read and trim the image from white borders
img = Image.open(input_file)
img = trim(img)
img = np.asarray(img)
cv2.imshow('trimmed',img)
# 
img = rescaling(img,input_file)
img = deskew(img) 
gray = get_grayscale(img)
img = remove_noise(gray)
result = get_Strings(img, gray)
if save_result:
    detection_results_file = os.path.join(result_folder, "Detection_Results.json")
    with open(detection_results_file, 'w') as f:
        json.dump(result, f,sort_keys=True,indent=4)
else:
    print("no Json output")



#cv2.imshow('img', img)
cv2.waitKey(100000)
if delete :
    os.remove(input_file)

#3,5
# show the output images
#cv2.imshow("Input", img)
##cv2.imshow("Output", thresh)
#cv2.waitKey(0)
