# Dockerfile for todolist frontend
FROM python:3.9-slim

WORKDIR /webapp

RUN pip install flask
RUN pip install requests

COPY . .

CMD ["python", "todolist.py"]