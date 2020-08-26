# Pytesseract-Opencv

An OCR that extract data from ID card using Opencv and Tesseract 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need Docker installed on your system and a command line editor.

```
Docker
Git Bash (on Windows)
Terminal (Linux or Mac)
```

### Installing and Running

You can clone this repository or download a zip file, build and run the Docker image.

```
$ docker build -t pytesseract-opencv .
$ docker run -d -p 5000:5000 pytesseract-opencv
```
Then open up browser to http://localhost:5000

### Heroku
for deploying docker image on Heroku follow these steps:

Log in to Container Registry:
```
$ heroku container:login
```
Then navigate to the app’s directory and create a Heroku app:
```
$ heroku create
```
Build the image and push to Container Registry:
```
$ heroku container:push web
```
Then release the image to your app:
```
$ heroku container:release web
```
Now open the app in your browser:
```
$ heroku open
```
### Closing Docker container

 for closing a Docker container, after running it :
```
 $ docker stop my_container
```
With my_container being either the container id or name. You can look at your running container’s property with the command:
```
 $ docker ps
```
or if you want to look at all your created containers:
```
 $ docker ps -a
```
 lastly if you want to delete a container:
```
 $ docker rm my_container
```

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


### How it works

The code can be divided in two part: the Ocr process and the web server process.

#### Ocr process

the Ocr process is started by a call to the run() method situated in __*src/ocr.py*__

```python
from ocr import run

run(image_path, thread_id)
```
it will take as argument *image_path* which is the path to the image to be processed and *thread_id* the id of the thread which will be running the task. the output is an opencv image (or numpy.array) of the grayscale image, and after the ocr is ended, it will write its result in __*results/Detection_Results{thread_id}.json*__.
the ocr process can be described by the steps below:

![Image of file system](https://github.com/youssef-e/Pytesseract-Opencv/blob/master/Documentation/images/schema1.png)

1. The ocr process start with image pre-processing : it trims the border, rescales the image and deskew it. after that, the image will be duplicated throught 20 threshold filters.
	In this step, Two files are called: __*src/ocr.py*__ which start the process, and __*Utils/Image_Process_Utils.py*__ which contain all the methods for image processing, along with __*Utils/Extract_Utils.py*__ which calling the method that applies the filters.

2. Tesseract will extract text from each one of the duplicated image, resulting in an array of 20 dictionaries that contains the fields of the id card for each image. 
	In this step, the files called are: __*Utils/Extract_Utils.py*__ that will call Tesseract, on each image, and call the extraction methods located in __*Utils/Classes/`*`*__.
	as each field has its own extraction method, and in order to make the code more readable, they are represented as objects in the Utils/Classes directory, with each field inheriting from the Fields class.

3. Each field is then averaged thanks to a system of coefficients whose values (per filter) are found in __*src/ocr.py*__. The averaging is also made in __*Utils/Extract_Utils.py*__, using the methods in __*Utils/Classes/`*`*__ objects and the result is retrieved by __*src/ocr.py*__ and  written in a JSON file( __*results/Detection_Results{thread_id}.json*__ )


4. __*src/Id_check*__ is then called after the ocr process is finished to check weither or not the content of __*results/Detection_Results{thread_id}.json*__ is syntaxically correct and then, if the MRZ is valid, will compare the fields with it.
```python
from Id_check import check

check(thread_id)
```
It will look for __*results/Detection_Results{thread_id}.json*__, read its data, and then check if the fields are syntaxically correct. if so, it will reconstitute The MRZ using the field and then compare it to the actual MRZ. it will also compare each field with its equivalent in the MRZ to try to correct minor error. Lastly it will write the results of each comparison in __*results/Id_check_Results{thread_id}.json*__ which can the be used along with __*results/Detection_Results{thread_id}.json*__ for the website in by __*app.py*__.
	
#### Web server process

The web server is made using Flask, an open-source web development framework in Python that is meant to be light, combined with a system of templates. the Templates are located in __*templates/*__ and are using Jinja2 to work. The routes are located in __*app.py*__:

- route: __*/analyse*__
  * input: deposited image
  * output: `{"Token" : "Task_id"}`
  create a thread that run the `run()` method from __*src/ocr.py*__, and then add it to **tasks**, a global dictionnary of thread, along with its *Task_id*. It will then create a json with the thread id

- route: __*/status/<Task_id>*__

  - check if Task_id exist in the **tasks** dictionnary and respond with an  `not found : 404` html code if it doesn't
  - check if __*results/Detection_Results{thread_id}.json*__  exist in __*results*__ and respond with `processing : 102` html code if it doesn't
  - run the `check()` method from __*src/Id_check*__ and then will check if __*results/Id_check_Results{thread_id}.json*__ contain the field `'error'`; it will show __*results/Id_check_Results{thread_id}.json*__ and respond with `Ok : 200` if no error is found or __*results/Detection_Results{thread_id}.json*__ otherwise.
  - either way it will then delete the two json files and then remove the thread from the **tasks** dictionnary