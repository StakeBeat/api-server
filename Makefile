start:
	pip install -e .
	FLASK_APP=routes.py FLASK_ENV=development flask run
