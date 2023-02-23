FROM python:3.10-buster

WORKDIR /root
COPY requirements.txt ./
COPY get-contributors.py /usr/bin/get-contributors

RUN chmod +x /usr/bin/get-contributors

RUN python3 -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf requirements.txt