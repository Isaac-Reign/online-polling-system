#!/user/bin/env bash

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser --no-input
	