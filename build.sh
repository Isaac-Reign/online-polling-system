#!/user/bin/env bash

set -o errexit
pip install -r requirements.txt

python manage.py migrate

if [[ $CREATE_SUPERUSER ]];
then
	python manage.py createsuperuser --no-input
fi	