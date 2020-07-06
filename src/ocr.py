# import the necessary packages
import argparse
import os
import sys
import json


def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

utils_path = os.path.join(get_parent_dir(1), "Utils")
sys.path.append(utils_path)



from Image_Process_Utils import(
    pdf_convertion,
    read_and_trim,
    rescaling,
    get_grayscale,
    remove_noise,
    apply_threshold,
    deskew,
    get_Strings
    )
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
    pdf_convertion(input_file, detection_results_folder+"/pdfToimage.png")
    input_file = detection_results_folder+"/pdfToimage.png"
    delete = True
#read and trim the image from white borders
img = read_and_trim(input_file)

img = rescaling(img,input_file,detection_results_folder)
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
if delete :
    os.remove(input_file)

input("Press Enter to continue...")
#3,5
# show the output images
#cv2.imshow("Input", img)
##cv2.imshow("Output", thresh)
#cv2.waitKey(0)
