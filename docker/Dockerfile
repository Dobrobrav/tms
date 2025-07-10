FROM python:3.13

RUN curl -Ls https://astral.sh/uv/install.sh | bash && mv /root/.local/bin/uv /usr/local/bin/

COPY /conf /usr/src/conf
WORKDIR /usr/src
RUN uv pip install --system -r conf/requirements.txt

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
WORKDIR /usr/src/app
ENTRYPOINT ["/entrypoint.sh"]
