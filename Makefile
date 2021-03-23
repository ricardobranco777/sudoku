test:
	@python3 -m unittest *_test.py
	@pylint *.py --disable=invalid-name,line-too-long
	@flake8 *.py --ignore=E501
