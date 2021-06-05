FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

#ENTRYPOINT python final_solution.py

RUN pip install --upgrade pip

RUN apt-get update ##[edited]

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get update && apt-get install -y python3-opencv

RUN apt-get update && apt-get install -y build-essential libzbar-dev

CMD ["python", "final_solution.py"]