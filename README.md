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
