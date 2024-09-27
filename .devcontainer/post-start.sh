poetry install --no-root --with dev

poetry run python -m django migrate
