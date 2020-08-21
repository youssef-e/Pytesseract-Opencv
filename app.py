from flask import Flask,render_template,request, redirect, url_for,g, abort,current_app
from werkzeug.exceptions import HTTPException, InternalServerError
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from threading import Thread
import time
import uuid
import os
import sys
import cv2
import json
import socket
import random
from datetime import datetime
src_path = os.path.join(".", "src")
sys.path.append(src_path)
from ocr import (run, get_parent_dir)
from Id_check import check
__author__ = 'Youssef Ellaabi <youssef.ellaabi@everycheck.fr>'
__source__ = ''

tasks={}
app = Flask(__name__)



UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = { 'pdf', 'png', 'jpg', 'jpeg'}
detection_results_folder = os.path.join(get_parent_dir(n=1), "results")
json_file = os.path.join(detection_results_folder ,"Detection_Result.json")

task_id=0;

@app.before_first_request
def before_first_request():
    """Start a background thread that cleans up old tasks."""
    def clean_old_tasks():
        """
        This function cleans up old tasks from our in-memory data structure.
        """
        global tasks
        while True:
            # Only keep tasks that are running or that finished less than 5
            # minutes ago.
            five_min_ago = datetime.timestamp(datetime.utcnow()) - 5 * 60
            tasks = {task_id: task for task_id, task in tasks.items()
                     if 'completion_timestamp' not in task or task['completion_timestamp'] > five_min_ago}
            time.sleep(60)

    if not current_app.config['TESTING']:
        thread = Thread(target=clean_old_tasks)
        thread.start()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def threaded_task(filepath,task_id):
   gray = run(filepath,task_id)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/layout")
def layout():
  return render_template("layout.html")

@app.route('/correct-data/<int:task_id>', methods = ['POST'])
def correct_data(task_id):
   data = request.form
   data = data.to_dict(flat=False)
   data.pop('submit', None)
   for c in data : 
      data[c] = data[c][0]
   detection_results_file = os.path.join(detection_results_folder, "Detection_Results{}.json".format(task_id))
   with open(detection_results_file, 'w') as f:
      json.dump(data, f,sort_keys=False,indent=4)
   print(data)
   check(task_id)
   return redirect(url_for('upload_file',task_id=task_id))

@app.route('/loading', methods = ['POST','GET'])
def load():
   global task_id
   if request.method == 'POST':
      f = request.files['file']
      # create a secure filename
      filename = secure_filename(f.filename)
      # save file to /static/uploads
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      try:
         f.save(filepath)
      except IsADirectoryError:
         return render_template("index.html")
      task_id = random.randrange(1000,9999)
      img=cv2.imread(filepath)
      imagename = "{}.png".format(task_id)
      ofilename = os.path.join(app.config['UPLOAD_FOLDER'],imagename)
      cv2.imwrite(ofilename, img)

      detection_results_file = os.path.join(detection_results_folder, "Detection_Results{}.json".format(task_id))
      tasks[task_id] = {'task_thread': Thread(target=threaded_task, args=(task_id,filepath)),
                        'filepath': filepath}
      tasks[task_id]['task_thread'].daemon = True
      tasks[task_id]['task_thread'].start()
      return render_template("loading.html",task_id=task_id)
   if request.method == 'GET':
      return render_template("loading.html",task_id=task_id)

@app.route('/loaded/<int:task_id>', methods = ['GET'])
def is_loaded(task_id):
   print(task_id)
   detection_results_file = os.path.join(detection_results_folder, "Detection_Results{}.json".format(task_id))
   print(detection_results_file)
   if os.path.exists(detection_results_file):
      return redirect(url_for('upload_file',task_id=task_id))
   else:
      # time.sleep(10)
      return render_template("loading.html",task_id=task_id)


@app.route('/uploader/<int:task_id>', methods = ['GET' , 'POST'])
def upload_file(task_id):
   imagename = "{}.png".format(task_id)
   ofilename = os.path.join(app.config['UPLOAD_FOLDER'],imagename)
   rslt = ""
   detection_results_file = os.path.join(detection_results_folder, "Detection_Results{}.json".format(task_id))
   id_check_results_file = os.path.join(detection_results_folder, "Id_check_Results{}.json".format(task_id))
   # perform OCR on the processed image‡
   check(task_id)
   with open(detection_results_file) as json_file:
      data = json.load(json_file)
   with open(id_check_results_file) as json_file:
      data_check = json.load(json_file)
   return render_template("uploaded.html", data=data, data_check=data_check, fname=imagename,task_id=task_id)

if __name__ == '__main__':
   hostname = socket.gethostname()
   ip_address = '0.0.0.0'
   app.run(host=ip_address, port=os.environ.get('PORT', 5000), debug=True )
