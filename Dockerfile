FROM ubuntu:20.04 

RUN apt-get update 
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install -y tesseract-ocr-fra python3-pip

COPY . /app

WORKDIR /app

RUN pip3 install scikit-build

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["app.py"]
