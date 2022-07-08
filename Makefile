install:
	@python -m pip install kapylan --upgrade

build:
	@python -m build

clean:
	@rm -rf build dist .eggs *.egg-info

tests:
	@python -m unittest discover -q