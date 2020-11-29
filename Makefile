.PHONY: black
black:
	poetry run black **/*.py $(BLACK_OPTIONS)

.PHONY: isort
isort:
	poetry run isort **/*.py --multi-line 3 --trailing-comma --line-width 88 --skip snapshots $(ISORT_OPTIONS)

.PHONY: autoflake
autoflake:
	poetry run autoflake -r $(AUTOFLAKE_OPTIONS) --exclude snapshots --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports **/*.py | tee autoflake.log
	echo "$(AUTOFLAKE_OPTIONS)" | grep -q -- '--in-place' || ! [ -s autoflake.log ]

.PHONY: lint
lint: ISORT_OPTIONS := --check-only
lint: BLACK_OPTIONS := --check
lint: autoflake isort black
	poetry run mypy **/*.py --ignore-missing-imports
	poetry run flake8 **/*.py

.PHONY: format
format: AUTOFLAKE_OPTIONS := --in-place
format: autoflake isort black