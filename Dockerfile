FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -U pip setuptools

RUN pip install .

EXPOSE 5000

COPY . .

CMD ["make", "start"]
