FROM ubuntu:18.04
LABEL maintainer="xelchantiry@my.bcit.ca"

ENV FILESYSTEM_ROOT="/app"

WORKDIR $FILESYSTEM_ROOT

RUN apt-get update -y && 
RUN apt-get install -y python3 
RUN apt-get install python3-pip
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]