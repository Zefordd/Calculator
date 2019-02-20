FROM python:3.6.7

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python main.py
