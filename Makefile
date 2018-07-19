all: build

build: clean
	python setup.py sdist bdist_wheel --universal > /dev/null

clean:
	rm -rf __pycache__/ build/ dist/ *.egg-info/
