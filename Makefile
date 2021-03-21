test:
	@TZ=UTC LC_ALL=en_US.UTF-8 python3 -m unittest *_test.py
	@pylint *.py --disable=invalid-name,line-too-long,too-many-public-methods
	@flake8 *.py --ignore=E501
