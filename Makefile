.PHONY: all lint test build clean

all: build

fmt:
	python -m black .

lint:
	python -m flake8

test:
	py.test

build: clean test lint fmt
	python setup.py sdist bdist_wheel --universal > /dev/null

clean:
	rm -rf __pycache__/ build/ dist/ *.egg-info/
