# Running the project
1. `uv sync` — install all dependencies.
2. From the project root, run `uv run python -m mlops_testing.prepare` to prepare the data.
3. From the project root, run `uv run python -m mlops_testing.train` to train the model and collect metrics.

# Running tests
`uv run pytest -v` — run all tests.

# Running the linter (ruff)
`uv run ruff check` — check the code for lint errors.
`uv run ruff check --fix` — autoformat the code.

# Contributing
1. Create a new branch from `main`:
   `git switch -c <type>/<short-description>`
   (e.g. `feat/add-metrics`, `fix/data-loading`)
2. Stage your changes:
   `git add <path>` (or `git add .` to stage everything)
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   `git commit -m "<type>(<scope>): <description>"`
   (e.g. `feat(train): save metrics to JSON`)
4. Push the branch to the remote:
   `git push -u origin <branch-name>`
   (after the first push, a plain `git push` is enough)
5. Open a pull request into `main`.