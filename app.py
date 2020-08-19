from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import os
import sys
import cv2
import json
import socket
import random
src_path = os.path.join(".", "src")
sys.path.append(src_path)
from ocr import (run, get_parent_dir)
from Id_check import check
__author__ = 'Youssef Ellaabi <youssef.ellaabi@everycheck.fr>'
__source__ = ''

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = { 'pdf', 'png', 'jpg', 'jpeg'}
detection_results_folder = os.path.join(get_parent_dir(n=1), "results")
detection_results_file = os.path.join(detection_results_folder, "Detection_Results.json")
id_check_results_file = os.path.join(detection_results_folder, "Id_check_Results.json")
json_file = os.path.join(detection_results_folder ,"Detection_Result.json")
current_image_number=0;

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/layout")
def layout():
  return render_template("layout.html")

@app.route('/correct-data', methods = ['POST'])
def correct_data():
   print("data :: ", request.form)
   data = request.form
   data = data.to_dict(flat=False)
   data.pop('submit', None)
   for c in data : 
      data[c] = data[c][0]
   with open(detection_results_file, 'w') as f:
      json.dump(data, f,sort_keys=False,indent=4)
   print(data)
   check()
   return redirect(url_for('upload_file'))


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   global current_image_number
   if request.method == 'POST':    
      # try:
      #    imagename = "{}.png".format(current_image_number)
      #    ofilename = os.path.join(app.config['UPLOAD_FOLDER'],imagename)
      #    os.remove(ofilename)
      # except (FileNotFoundError, UnboundLocalError):
      #    print('no file to remove')

      f = request.files['file']
      # create a secure filename
      filename = secure_filename(f.filename)
      # save file to /static/uploads
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      try:
         f.save(filepath)
      except IsADirectoryError:
         return render_template("index.html")
      
      # load the example image and convert it to grayscale
      gray = run(filepath)

      # save the processed image in the /static/uploads directory
      current_image_number = random.randrange(1000,9999)
      imagename = "{}.png".format(current_image_number)
      ofilename = os.path.join(app.config['UPLOAD_FOLDER'],imagename)
      cv2.imwrite(ofilename, gray)
      print("ofilename::",ofilename)
      print("imagename",imagename)
      print("filename::",filename)

      rslt = ""
      # perform OCR on the processed image
      with open(detection_results_file) as json_file:
         data = json.load(json_file)
      check()
      with open(id_check_results_file) as json_file:
         data_check = json.load(json_file)
      
      os.remove(filepath)
      return render_template("uploaded.html", data=data,data_check=data_check, fname=imagename)
      
   if request.method == 'GET':
      imagename = "{}.png".format(current_image_number)
      ofilename = os.path.join(app.config['UPLOAD_FOLDER'],imagename)
      rslt = ""
      # perform OCR on the processed image
      with open(detection_results_file) as json_file:
         data = json.load(json_file)
      with open(id_check_results_file) as json_file:
         data_check = json.load(json_file)
      # os.remove(ofilename)
      return render_template("uploaded.html", data=data, data_check=data_check, fname=imagename)

if __name__ == '__main__':
   hostname = socket.gethostname()
   ip_address = '0.0.0.0'
   app.run(host=ip_address, port=os.environ.get('PORT', 5000), debug=True)
