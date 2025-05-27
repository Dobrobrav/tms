FROM python:3.13

COPY /conf /usr/src/conf
WORKDIR /usr/src
RUN pip install -r conf/requirements.txt

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
WORKDIR /usr/src/app
ENTRYPOINT ["/entrypoint.sh"]
