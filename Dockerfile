FROM ubuntu:14.04

MAINTAINER ldqsmile@Gmail.com
ENV LC_ALL C.UTF-8

### APT source list
# RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

### Install pip
RUN apt-get update \
    && apt-get install -y python-pip

### Install wxpy and qqbot
RUN pip install -U wxpy \
    && pip install qqbot \
    && pip install flask

COPY src/start.sh /start.sh
COPY src/* /bots/
RUN mkdir /bots/logs \
    && chmod +x /start.sh \
    && chmod -R 777 /bots

EXPOSE 8189
WORKDIR /bots
CMD ["/start.sh"]