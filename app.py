from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import sys
import cv2
import json
import socket
src_path = os.path.join(".", "src")
sys.path.append(src_path)
from ocr import (run, get_parent_dir)
__author__ = 'Youssef Ellaabi <youssef.ellaabi@everycheck.fr>'
__source__ = ''

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
detection_results_folder = os.path.join(get_parent_dir(n=1), "results")
detection_results_file = os.path.join(detection_results_folder, "Detection_Results.json")
json_file = os.path.join(detection_results_folder ,"Detection_Result.json")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']

      # create a secure filename
      filename = secure_filename(f.filename)
      # save file to /static/uploads
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      f.save(filepath)
      
      # load the example image and convert it to grayscale
      gray = run(filepath)

      # save the processed image in the /static/uploads directory
      imagename = "{}.png".format(os.getpid())
      ofilename = os.path.join(app.config['UPLOAD_FOLDER'],imagename)
      cv2.imwrite(ofilename, gray)
      print("ofilename::",ofilename)
      print("imagename",imagename)
      print("filename::",filename)

      rslt = ""
      # perform OCR on the processed image
      with open(detection_results_file) as json_file:
         data = json.load(json_file)
      for c in data:
         rslt += c +" : "+ data[c] + "\n"

      # os.remove(ofilename)
      os.remove(filepath)
      return render_template("uploaded.html", displaytext= rslt, fname=imagename)
      # remove the processed image

   if request.method == 'GET':
      imagename = "{}.png".format(os.getpid())
      ofilename = os.path.join(app.config['UPLOAD_FOLDER'],imagename)
      rslt = ""
      # perform OCR on the processed image
      with open(detection_results_file) as json_file:
         data = json.load(json_file)
      for c in data:
         rslt += c +" : "+ data[c] + "\n"
      # os.remove(ofilename)
      return render_template("uploaded.html", displaytext= rslt, fname=imagename)

if __name__ == '__main__':
   hostname = socket.gethostname()
   ip_address = socket.gethostbyname('localhost')
   app.run(host=ip_address, port=5000, debug=True)
