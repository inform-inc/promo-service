FROM python:3
# ADD . /promo-service

WORKDIR /usr/src/app
# COPY requirements.txt /usr/src/app/requirements.txt
# COPY /requirements.txt .

#COPY . /usr/src/app/
COPY . .

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt



CMD [ "python","-u","./main.py" ]