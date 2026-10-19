# mlops-testing

## Setup
1. `uv sync` — install all dependencies.
2. `uv run pre-commit install` — install git hooks (once after cloning).
   Hooks live in `.git/hooks/`, which is not versioned, so every clone needs this step.

## Running the pipeline
The pipeline is managed by [DVC](https://dvc.org/) and described in `dvc.yaml`:
`prepare` (load and split data) → `train` (train the model and compute metrics).

Run the whole pipeline from the project root:
```bash
uv run dvc repro
```
DVC re-runs only the stages whose code, data or parameters changed
and records the exact state of every input and output in `dvc.lock`.

Hyperparameters live in `params.yaml`: change them there, not in the code.

After the pipeline changes, commit `dvc.lock` and `metrics/metrics.json`
together with the code, so every commit points to its own data, model and metrics.

### Metrics
- `uv run dvc metrics show` — show current metrics.
- `uv run dvc metrics diff` — compare metrics with the last commit.
- `uv run dvc params diff` — compare parameters with the last commit.

### Running a single stage manually (debugging only)
```bash
uv run python -m mlops_testing.prepare
uv run python -m mlops_testing.train
```
This bypasses DVC: `dvc.lock` is not updated and outputs are not cached.

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
- commit message format (Conventional Commits);
- secrets in commit.

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
