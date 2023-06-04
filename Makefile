venv/bin/activate:
	python -m venv venv

setup:
	. venv/bin/activate;
	pip install -r requirements.txt

migrate:
	. venv/bin/activate;
	python manage.py migrate;

run:
	. venv/bin/activate;
	python manage.py runserver
