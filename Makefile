.PHONY: install
install:
	pre-commit install
	poetry install
	poetry shell

.PHONY: install-pre-commit-mac-os
install-pre-commit-mac-os:
	@if brew ls --versions pre-commit > /dev/null; then \
		echo "Pre commit is installed."; \
		else brew install pre-commit; \
	fi

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files

.PHONY: run
run:
	python main.py data/input/example.txt data/output -p -s

.PHONY: count-lines
count-lines:
	pygount --format=summary .

.PHONY: unit-test
unit-test:
	poetry run pytest
