FROM python:3.9.6

# Setup ENV variables
ENV DOCKERIZE_VERSION v0.6.1
ENV PYTHONUNBUFFERED 1
ENV PATH $PATH:/usr/src/.local/bin
ENV DOCKER_BUILDKIT 0
ENV COMPOSE_DOCKER_CLI_BUILD 0

# Set workspace
WORKDIR /usr/src

# Install dockerize
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
  && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
  && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Copy code and install app dependencies
COPY . /usr/src

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN adduser user
USER user