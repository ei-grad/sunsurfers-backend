FROM ubuntu

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y \
    git \
    python3 \
    python3-dev \
    python3-pip \
    libgeos-dev \
    libgdal-dev \
    python3-psycopg2 \
    python3-lxml \
    python3-cairosvg \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/usr/src/app
WORKDIR /usr/src/app

ADD AmaticSC-Regular.ttf /usr/share/fonts/TTF/

COPY requirements.txt /usr/src/app/
RUN pip3 install -r /usr/src/app/requirements.txt

CMD ["gunicorn", "--user", "www-data", "--worker-class", "gevent", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8000", "sunsurfers.wsgi:application"]

COPY . /usr/src/app
