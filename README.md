# mlops-testing

## Running the project
1. `uv sync` — install all dependencies.
2. From the project root, run `uv run python -m mlops_testing.prepare` to prepare the data.
3. From the project root, run `uv run python -m mlops_testing.train` to train the model and collect metrics.

## Running tests
`uv run pytest -v` — run all tests.

## Linting and formatting (ruff)
- `uv run ruff check` — check the code for lint errors.
- `uv run ruff check --fix` — apply automatic lint fixes (e.g. sort imports).
- `uv run ruff format` — format the code.

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
4. Push the branch to the remote (after the first push, a plain `git push` is enough):
```bash
   git push -u origin <branch-name>
```
5. Open a pull request into `main`.
