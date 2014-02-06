target=build
source=src
python=PYTHONPATH=./$(target):$(PYTHONPATH) python
nose=$(python) ./$(source)/nose/bin/nosetests

init: clean setup test

setup:
	pip install -r requirements.txt -t $(target) -b $(source)

clean:
	rm -rf $(source) $(target) .ropeproject .coverage junit-report.xml
	find . -type f -name "*.pyc" -exec rm -v {} \;

test:
	$(nose) -v --with-coverage --cover-package=maxcdn \
		./test/test.py

travis: setup
	$(nose) -v  --with-xunit --xunit-file=junit-report.xml \
		./test/test.py

test/help:
	$(nose) --help | less

.PHONY: init clean test coverage test/help
