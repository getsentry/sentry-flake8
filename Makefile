.PHONY: all lint test build clean

all: build

lint:
	true

test:
	true

build: clean test lint
	python setup.py sdist bdist_wheel --universal > /dev/null

clean:
	rm -rf __pycache__/ build/ dist/ *.egg-info/
