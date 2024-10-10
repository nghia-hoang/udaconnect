FROM python:3.8-alpine

WORKDIR .

RUN apk add --update --no-cache \
    gcc \
    linux-headers \
    make \
    geos \
    musl-dev \
    g++ \
    libc-dev \
    postgresql-dev \
    libpq \
    geos-dev
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install protobuf==5.27.2
RUN pip install --upgrade pip
EXPOSE 5000

COPY . .
CMD ["python", "main.py"]
