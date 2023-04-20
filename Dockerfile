FROM python:3.9.13-slim-buster

# Set the working directory inside the container
WORKDIR /powertofly/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install psycopg2 dependencies, java 11 installation
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2 \
    && apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get install -y --no-install-recommends openjdk-11-jre && \
    apt-get install ca-certificates-java -y && \
    apt-get clean && \
    update-ca-certificates -f;

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

# Download and copy the PostgreSQL JDBC driver JAR file
ADD https://jdbc.postgresql.org/download/postgresql-42.6.0.jar /opt/postgresql-jdbc-driver.jar

# Set the SPARK_CLASSPATH environment variable to include the JDBC driver
ENV SPARK_CLASSPATH /opt/postgresql-jdbc-driver.jar

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
COPY powertofly.py init_database.sh /powertofly/

ENTRYPOINT ["python3", "powertofly.py"]
