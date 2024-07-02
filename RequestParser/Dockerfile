FROM python:3.12
WORKDIR /app/request_parser
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "main.py"]