FROM python:3.8-slim as production

ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"
COPY ./requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y gcc musl-dev libxml2-dev libpq5 libxslt-dev --no-install-recommends apt-utils

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./app /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser --disabled-password --gecos '' user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]

