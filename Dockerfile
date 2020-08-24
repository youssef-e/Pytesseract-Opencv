FROM python:3.7.9-buster

RUN apt update && apt install -y libsm6 libxext6

RUN apt-get -y install tesseract-ocr-fra

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]