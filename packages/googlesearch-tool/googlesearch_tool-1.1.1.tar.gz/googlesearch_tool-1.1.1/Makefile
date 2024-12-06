.PHONY: clean build publish test

clean:
	rm -rf build dist *.egg-info

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

test:
	python -m pytest tests/ 