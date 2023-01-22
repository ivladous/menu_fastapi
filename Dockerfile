#
FROM python:3.10-slim

#
WORKDIR /webapp

#
COPY ./requirements.txt .

#
RUN pip install --no-cache-dir --upgrade -r /webapp/requirements.txt

#
COPY . .
