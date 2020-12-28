FROM nginx:1.18.0-alpine

COPY ./app.conf /etc/nginx/conf.d
COPY ./uwsgi_params /etc/nginx/uwsgi_params

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static