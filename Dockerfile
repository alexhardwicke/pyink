FROM python:3.6

VOLUME /config/

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
  ink

RUN pip3 install pyyaml

COPY . .

CMD [ "python", "-m", "pyink" ]
