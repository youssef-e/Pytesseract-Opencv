# Pytesseract-Opencv

An OCR that extract data from ID card using Opencv and Tesseract 

# OCR Tesseract Docker
Allows upload of an image for OCR using Tesseract and deployed using Docker.  This uses Flask, a light weight web server framework - but for development purposes only.  OpenCV is used to reduce noise in the image for better processing by pytesseract.

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
$ docker run -d -p 5000:5000 pytesseract-opencv .
```

OR you can pull and/or run the Docker image from my repository on Docker Hub

```
docker pull yellaabi/pytesseract-opencv
docker run -d -p 5000:5000 yellaabi/pytesseract-opencv
```
Then open up browser to http://localhost:5000
