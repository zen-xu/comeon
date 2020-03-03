clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

format:
	@poetry run autoflake \
		--in-place \
		--recursive \
	    --remove-duplicate-keys \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		--remove-unused-variables \
		comeon/
	@poetry run black comeon/ tests/
	@poetry run isort --recursive comeon/

test:
	@poetry run pytest --cov=comeon -sq tests/ 

build:
	@poetry build

publish:
	@poetry publish

wheel:
	@poetry build -v