FROM python:3.9.13-slim-buster

# Set the working directory inside the container
WORKDIR /powertofly/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Copy requirements from local to docker image
COPY requirements.txt /powertofly/requirements.txt

# Install the dependencies in the docker image
RUN python3 -m venv $VIRTUAL_ENV
RUN pip3 install -r requirements.txt --no-cache-dir

# Copy everything from the current dir to the image
COPY app /powertofly/app
COPY config /powertofly/config
COPY migrations /powertofly/migrations
COPY redoc /powertofly/redoc
COPY tests /powertofly/tests
COPY .db.env .env .redis.env powertofly.py init_database.sh /powertofly/

# expose port and run entrypoint.sh
#ENTRYPOINT ["/powertofly/entrypoint.sh"]
ENTRYPOINT ["python3", "powertofly.py"]
