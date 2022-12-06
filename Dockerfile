FROM nvcr.io/nvidia/tensorflow:22.11-tf2-py3

COPY pyfiles /tmp
COPY requirements.txt /tmp
WORKDIR /tmp

RUN pip install -r requirements.txt


