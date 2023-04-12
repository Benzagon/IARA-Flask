FROM python:3.10.10

RUN apt update && apt install libgl1 -y

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# COPY . /app

COPY . .

EXPOSE 8000

CMD [ "python" , "Server.py" ]