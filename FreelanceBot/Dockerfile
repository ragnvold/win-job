FROM python:3.12
WORKDIR /app/freelance_bot
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python", "main.py"]