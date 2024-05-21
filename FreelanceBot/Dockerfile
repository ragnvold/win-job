FROM python:3.12
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade setptools
RUN pip3 install -r requirements.txt
COPY . .