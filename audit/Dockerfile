FROM ubuntu:18.04
LABEL maintainer="mmulder10@bcit.ca"

ENV FILESYSTEM_ROOT="/app"
ENV HOSTNAME = "ec2-34-219-221-192.us-west-2.compute.amazonaws.com"

WORKDIR $FILESYSTEM_ROOT

RUN apt-get update -y && \
apt-get install -y python3 python3-pip
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]