.PHONY: validate diarios-index

PYTHON ?= python3

validate:
	$(PYTHON) tools/validate_brh.py

diarios-index:
	$(PYTHON) tools/generate_diarios_index.py
