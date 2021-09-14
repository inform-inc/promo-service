FROM python:3
# ADD . /promo-service
WORKDIR /usr/src/app

# COPY requirements.txt /

COPY . .

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt



CMD [ "python", "./main.py" ]