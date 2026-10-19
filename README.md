# mlops-testing

## Setup
1. `uv sync` — install all dependencies.
2. `uv run pre-commit install` — install git hooks (once after cloning).
   Hooks live in `.git/hooks/`, which is not versioned, so every clone needs this step.

## Running the project
From the project root:
1. `uv run python -m mlops_testing.prepare` — prepare the data.
2. `uv run python -m mlops_testing.train` — train the model and collect metrics.

## Running tests
`uv run pytest -v` — run all tests.

## Linting and formatting (ruff)
- `uv run ruff check` — check the code for lint errors.
- `uv run ruff check --fix` — apply automatic lint fixes (e.g. sort imports).
- `uv run ruff format` — format the code.

## Pre-commit hooks
Hooks run automatically on every `git commit` and check only staged files:
- ruff lint and format;
- file hygiene: trailing whitespace, final newline, YAML syntax, large files;
- commit message format (Conventional Commits).

Run all hooks on the whole project manually:
`uv run pre-commit run --all-files`

If a commit fails because a hook modified files, review the changes,
stage them again with `git add` and repeat the commit.

## Contributing
1. Create a new branch from `main`:
```bash
   git switch -c <type>/<short-description>
```
   For example: `feat/add-metrics`, `fix/data-loading`.
2. Stage your changes (or use `git add .` to stage everything):
```bash
   git add <path>
```
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
```bash
   git commit -m "<type>(<scope>): <description>"
```
   For example: `feat(train): save metrics to JSON`.
   The commit message format is checked by a pre-commit hook.
4. Push the branch to the remote (after the first push, a plain `git push` is enough):
```bash
   git push -u origin <branch-name>
```
5. Open a pull request into `main`.
