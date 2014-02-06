# Setup
###
target=build
source=src

pypath=PYTHONPATH=./$(target):$(PYTHONPATH)

nose=./$(source)/nose/bin/nosetests

tests=./test/test.py
test_opts=-v --with-coverage --cover-package=maxcdn


# Tasks
###
init: clean setup test

setup:
	pip install -r requirements.txt -t $(target) -b $(source)

clean:
	rm -rf $(source) $(target) .ropeproject .coverage junit-report.xml
	find . -type f -name "*.pyc" -exec rm -v {} \;

test:
	$(pypath) python $(nose) $(test_opts) $(tests)

test/help:
	$(nose) --help | less

# TODO: support 3.x
#test/32:
	#$(pypath) python3.2 $(nose) $(test_opts) $(tests)

#test/33:
	#$(pypath) python3.3 $(nose) $(test_opts) $(tests)

travis: setup
	$(pypath) python $(nose) -v --with-xunit --xunit-file=junit-report.xml \
		$(tests)

.PHONY: init clean test coverage test/help test/32 test/33

