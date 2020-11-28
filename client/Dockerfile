FROM alpine:latest
RUN apk update && apk add --no-cache supervisor py-pip
RUN mkdir -p /app /var/log/supervisor
RUN pip install websockets
COPY client.py /app/
COPY supervisord.conf /etc/supervisor/supervisord.conf
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]