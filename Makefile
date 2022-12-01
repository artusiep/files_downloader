pre-commit:
	poetry run pre-commit run --all-files

run:
	python main.py data/input/example.txt data/output -p -s
