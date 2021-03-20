#!/bin/bash

rm -rf readaloudapi/migrations

rm db.sqlite3

python3 manage.py migrate

python3 manage.py makemigrations readAloudapi
python3 manage.py migrate readAloudapi

python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata profiles
python3 manage.py loaddata skills
python3 manage.py loaddata topics
python3 manage.py loaddata vocab
python3 manage.py loaddata books
python3 manage.py loaddata book_skills
python3 manage.py loaddata book_topics
python3 manage.py loaddata book_vocabs
python3 manage.py loaddata questions
python3 manage.py loaddata comments



