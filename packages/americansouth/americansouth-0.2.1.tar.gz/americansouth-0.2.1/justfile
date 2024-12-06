set shell := ["bash", "-uec"]

default:
    @just --list

test:
    pytest -v

fmt:
    ruff format .
    ruff check --fix
    prettier --ignore-path=.prettierignore --config=.prettierrc.json --write .
    just --unstable --fmt
