FROM python:3.11.1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

RUN apt-get update
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]