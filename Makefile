# Setup
###
target=$(PWD)/build
source=$(PWD)/src

pypath=PYTHONPATH=$(target):./maxcdn:$(PYTHONPATH)

nose_opts=-v
nose=python $(source)/nose/bin/nosetests
cov_opts= --with-coverage --cover-package=maxcdn

tests=./test/test.py
int=./test/int.py

# Tasks
###
init: clean setup test

setup: distribute
	pip install -r requirements.txt -t $(target) -b $(source)

clean:
	rm -rf $(source) $(target) .ropeproject .coverage junit-report.xml
	find . -type f -name "*.pyc" -exec rm -v {} \;

coverage: build/coverage
	$(pypath) python $(nose) $(cov_opts) $(tests)

test:
	$(pypath) python $(tests)

test/2:
	# python 2.x
	$(pypath) python2 $(tests)

test/32:
	# python 3.2
	$(pypath) python3.2 $(tests)

test/33:
	# python 3.3
	$(pypath) python3.3 $(tests)

test/34:
	# python 3.4
	$(pypath) python3.4 $(test_opts) $(tests)

test/all:
	-make test/2
	-make test/32
	-make test/33
	-make test/34

nose: build/nose
	$(pypath) $(nose) $(nose_opts) $(tests)

nose/int: build/nose
	$(pypath) $(nose) $(nose_opts) $(int)

nose/all: nose nose/int

int:
	$(pypath) python $(test_opts) $(int)

int/2:
	# python 2.x
	$(pypath) python2 $(test_opts) $(int)

int/32:
	# python 3.2
	$(pypath) python3.2 $(test_opts) $(int)

int/33:
	# python 3.3
	$(pypath) python3.3 $(test_opts) $(int)

int/34:
	# python 3.4
	$(pypath) python3.4 $(test_opts) $(int)

int/all:
	-make int/2
	-make int/32
	-make int/33
	-make int/34

travis: setup test

distribute:
	pip install distribute

build/coverage:
	pip install coverage -t $(target) -b $(source)

build/nose:
	pip install nose -t $(target) -b $(source)

.PHONY: init clean test coverage test/help test/32 test/33
