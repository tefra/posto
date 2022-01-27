FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -U pip setuptools

RUN pip install .

EXPOSE 5000

CMD ["make", "start"]
