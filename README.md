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
