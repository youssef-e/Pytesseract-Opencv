# Documentation

This is a brief documentation explaining how this project works.

## Description

This project is an implementation of Tesseract OCR for ID card's fields extraction. The goal was to be able to upload an image of an id card in the website,
and then to get a json file with all the extracted informations.

### Dependencies
This project being written with python, it uses several librairies to make it work:

- Pytesseract a wrapper of Tesseract for python
- Opencv and PIL and numpy for image processing 
- Flask, and from werkzeug are used for the server, along with
  - jinja2 for the templating
  - Bootstrap
  - jquerry
  - poppers

### File system

![Image of file system](https://github.com/youssef-e/Pytesseract-Opencv/blob/master/Documentation/images/fileSystem.png)

### How it works

The code can be divided in two part: the Ocr process and the web server process.

#### Ocr process

the Ocr process is started by a call to the run() method situated in __*src/ocr.py*__

```
from ocr import run

run(image_path, thread_id)
```
it will take as argument *image_path* which is the path to the image to be processed and *thread_id* the id of the thread which will be running the task. the output is an opencv image (or numpy.array) of the grayscale image, and after the ocr is ended, it will write its result in __*results/Detection_Results{thread_id}.json*__
the ocr process start with image pre-processing : it trims the border, rescales the image and deskew it. after that, the image will be duplicated throught 20 threshold filters, and tesseract will extract text from each one of the duplicated image, resulting in an array of 20 dictionaries that contains the fields of the id card for each image. each field is then averaged thanks to a system of coefficients whose values (per filter) are found in ocr.py
finally the result is written on a JSON file( __*results/Detection_Results{thread_id}.json*__ )

![Image of file system](https://github.com/youssef-e/Pytesseract-Opencv/blob/master/Documentation/images/schema1.png)

The methods used for image processing are found in __*Utils/Image_Process_Utils.py*__ and the methods used for extracting the fields from the images and then averaging them are found in __*Utils/Extract_Utils.py*__
as each field has its own extraction method, and in order to make the code more readable, they are represented as objects in the Utils/Classes directory, with each field inheriting from the Fields class.

__*src/Id_check*__ is then called after the ocr process is finished to check weither or not the content of __*results/Detection_Results{thread_id}.json*__ is syntaxically correct and then if the MRZ is valid, will compare the fields with it.
the method called is check(), and only take as argument the thread_id, and will write its results in __*results/Id_check_Results{thread_id}.json*__
```
from Id_check import check

check(thread_id)
```
it will the look for __*results/Detection_Results{thread_id}.json*__, read its data, and then check if the fields are syntaxically correct. if so, it will reconstitute The MRZ using the field and then compare it to the actual MRZ. it will also compare each field with its equivalent in the MRZ to try to correct minor error. Lastly it will write the results of each comparison in __*results/Id_check_Results{thread_id}.json*__

#### Web server process
