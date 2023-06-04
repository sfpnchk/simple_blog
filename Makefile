venv/bin/activate:
	python -m venv venv

migrate :
	. venv/bin/activate;
	python manage.py migrate;

setup:
	. venv/bin/activate;
	pip install -r requirements.txt;
	python manage.py migrate;


run:
	. venv/bin/activate;
	python manage.py runserver
