.PHONY: validate

PYTHON ?= python3

validate:
	$(PYTHON) tools/validate_brh.py
