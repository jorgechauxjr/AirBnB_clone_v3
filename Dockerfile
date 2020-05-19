
FROM ubuntu:14.04
MAINTAINER Sebastian Lopez <1182@holbertonschool.com>

RUN apt-get update

# curl/wget/git
RUN apt-get install -y curl wget git

# Python
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
RUN cd /usr/src ; wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz ; tar xzf Python-3.4.3.tgz ; cd Python-3.4.3 ; ./configure ; make altinstall
# be sure it's 3.4 and not 3.5
RUN ! ls /usr/bin/python3.4 && ls /usr/src/Python-3.4.3/python && cp /usr/src/Python-3.4.3/python /usr/bin/python3.4 ; exit 0
# replace python version to have 3.4.4 as default
RUN rm -f /usr/bin/python
RUN rm -f /usr/bin/python3
RUN ln -s /usr/bin/python3.4 /usr/bin/python
RUN ln -s /usr/bin/python3.4 /usr/bin/python3
# Pip
RUN apt-get install -y python3-pip
RUN pip3 uninstall pep8 ; pip3 install pep8 ; pip3 install --upgrade pep8
# check if pep8 is correctly installed
RUN ! ls /usr/bin/pep8 && ls /usr/lib/python3.4/dist-packages/pep8.py && cp /usr/lib/python3.4/dist-packages/pep8.py /usr/bin/pep8 && chmod u+x /usr/bin/pep8 && sed -i '1 s/^.*$/#!\/usr\/bin\/python3/g' /usr/bin/pep8 ; exit 0

# Pip dependencies
RUN pip3 install numpy==1.15.0
RUN pip3 install SQLAlchemy
RUN pip3 install sqlalchemy
RUN pip3 install sqlalchemy --upgrade
RUN apt-get install -y libmysqlclient-dev
RUN pip3 install mysqlclient==1.3.10
RUN pip3 install Flask
RUN apt-get install -y python3-lxml
RUN pip3 install flask_cors
RUN pip3 install flasgger
RUN pip3 uninstall -y jsonschema ; pip3 install jsonschema==3.0.1

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

WORKDIR /code
COPY . .
CMD ["/entrypoint.sh"]