.PHONY: lint mkdocs-serve mkdocs-build mkdocs-clean

lint:
	pre-commit run --all-files # Uses pyproject.toml

mkdocs-clean:
	rm site/

mkdocs-serve:
	mkdocs serve

mkdocs-build:
	mkdocs build
