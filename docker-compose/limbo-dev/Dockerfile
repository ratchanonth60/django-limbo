FROM noobmaster666/limbo-template:latest

# RUN apt install systemctl -y

WORKDIR /app
COPY ../../requirements.txt /app/requirements.txt
COPY ../../ /app/limbo
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# # copy entry point to container
# COPY ../../entrypoint.sh /usr/local/bin/entrypoint.sh
# RUN chmod +x /usr/local/bin/entrypoint.sh
# COPY ../../celery.service /etc/systemd/system/celery.service
#
LABEL application=limbo

WORKDIR /app/limbo

