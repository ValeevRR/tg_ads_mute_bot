FROM python:3.13

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY src /app

EXPOSE 8080
CMD [ "python", "main.py" ]