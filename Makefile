.PHONY: all lint test build clean

all: build

fmt lint:
	pre-commit run --all-files --show-diff-on-failure

test:
	pytest

build: clean test fmt
	pip install -U wheel
	python setup.py sdist bdist_wheel > /dev/null

clean:
	rm -rf __pycache__/ build/ dist/ *.egg-info/
