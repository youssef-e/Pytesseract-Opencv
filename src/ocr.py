# import the necessary packages
import argparse
import os
import sys
import json


def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current working directory."""

    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

utils_path = os.path.join(get_parent_dir(1), "Utils")
sys.path.append(utils_path)

from Utils import (
    pdf_convertion,
  )
from Extract_Utils import get_Strings

from Image_Process_Utils import(
    read_and_trim,
    rescaling,
    get_grayscale,
    remove_noise,
    deskew,
    pre_process
    )


#~~~~~~~~~~~~~~ Main function ~~~~~~~~~~~~~~~~~#
#variable declaration
detection_results_folder = os.path.join(get_parent_dir(n=1), "results")
sample_image_folder = os.path.join(get_parent_dir(n=1), "sample_image")
sample_image = os.path.join(sample_image_folder, "_%6777622.jpg")

#id fields score
scores1={
          12 : 4,
          14 : 4,
          11 : 2,
          9 : 0.1,
          8 : 0.1,
          7 : 0.1,
          6 : 0.1,
          5 : 0.1,
          4 : 0.1,
          3 : 0.1,
          2 : 0.1
    }
#mrz scores
scores2={
          11 : 4,
          12 : 2,
          19 : 1,
          8 : 0.2,
          7 : 0.2,
          6 : 0.2,
          5 : 0.2,
          4 : 0.2,
          3 : 0.2,
          2 : 0.2,
    }
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-i", "--image",
    type=str,
    default=sample_image,
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
def run( input_f = input_file): 
  print("input_file::",input_f)
  if(input_f.split(".")[len(input_f.split("."))-1]=="pdf"):
    pdf_convertion(input_f, detection_results_folder+"/pdfToimage.png")
    input_f = detection_results_folder+"/pdfToimage.png"
    #delete = True
  #read and trim the image from white borders
  img = read_and_trim(input_f)
  (img,gray) = pre_process(img, input_f)
  result = get_Strings(img, gray, scores1,scores2)
  if save_result:
    detection_results_file = os.path.join(result_folder, "Detection_Results.json")
    with open(detection_results_file, 'w') as f:
      json.dump(result, f,sort_keys=False,indent=4)
    return gray
  else:
    print("no Json output")
    return gray



  # #cv2.imshow('img', img)
  # if delete :
  #   os.remove(input_f)

  #input("Press Enter to continue...")
#3,5
# show the output images
#cv2.imshow("Input", img)
##cv2.imshow("Output", thresh)
#cv2.waitKey(0)
