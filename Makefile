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

nose: build/nose
	$(pypath) $(nose) $(nose_opts) $(tests)

nose/int: build/nose
	$(pypath) $(nose) $(nose_opts) $(int)

test:
	$(pypath) python $(tests)

test/32:
	$(pypath) python3.2 $(tests)

test/33:
	$(pypath) python3.3 $(tests)

int:
	$(pypath) python $(test_opts) $(int)

travis: setup test

distribute:
	pip install distribute

build/coverage:
	pip install coverage -t $(target) -b $(source)

build/nose:
	pip install nose -t $(target) -b $(source)

.PHONY: init clean test coverage test/help test/32 test/33
