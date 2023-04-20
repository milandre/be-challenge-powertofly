BE Challenge PowerToFly
=======================
An API endpoint challenge for PowerToFly using Flask framework.

You will find [here](https://gist.github.com/scabbiaza/82e9069cfa71c4d7aa9d9539a794a1db) a specific list of requirements for this challenge.

## Requirements
* [Python 3.9+](https://www.python.org/downloads/)
* [Postgres 14.4](https://www.postgresql.org/docs/14/tutorial-install.html)
* [Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Redis](https://redis.io/docs/getting-started/installation/)

## Initial Setup

#### Local

You have to create .env, .db.env, .redis.env files using .example* files as a start.

If you are running the project for the first time, run:
```console
make run-local-init
```

After that, you can start your project with:
```console
make run-local
```

Launch [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

#### Local with Docker & Docker Compose

If you are running the project for the first time, you must run:
```console
make run-docker-init
```

After that, you can start your containers with:
```console
make run-docker
```

## Tests

#### Local

Run:
```console
make run-local-test
```

#### Local with Docker & Docker Compose

Run:
```console
make run-docker-test
```

## Pre-commit install

Run:
```console
make pre-commit-install
```
