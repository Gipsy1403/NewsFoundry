PYTHON=backend/.venv/Scripts/python.exe

.PHONY: test test-backend test-backend-verbose test-backend-cov

test: test-backend

test-backend:
	$(PYTHON) -m pytest -q

test-backend-verbose:
	$(PYTHON) -m pytest -v

test-backend-cov:
	$(PYTHON) -m pytest --cov
