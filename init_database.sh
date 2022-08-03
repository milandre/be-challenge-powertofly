#! /usr/bin/env sh

flask recreate-db
flask setup-dev
flask add-fake-data -n 2000000
