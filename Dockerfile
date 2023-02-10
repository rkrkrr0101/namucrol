FROM python:slim-buster
#FROM selenium/standalone-chrome:102.0
WORKDIR /usr/src
RUN apt-get -y update
RUN apt-get -y install wget
RUN apt-get -y install unzip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb



RUN pip install pymysql
RUN pip install selenium
RUN pip install webdriver-manager
RUN pip install python-dotenv
RUN pip install cryptography

COPY . ./app
CMD [ "python", "app/main.py" ]