# mlops-testing

## Setup
1. `uv sync` — install all dependencies.
2. `uv run dvc pull` — download data and model from DVC remote storage.
3. `uv run pre-commit install` — install git hooks (once after cloning).
   Hooks live in `.git/hooks/`, which is not versioned, so every clone needs this step.

## Running the pipeline
The pipeline is managed by [DVC](https://dvc.org/) and described in `dvc.yaml`:
`prepare` (load and split data) → `train` (train the model and compute metrics).

Start the MLflow tracking server first (see [Experiment tracking](#experiment-tracking-mlflow)),
then run the whole pipeline from the project root:
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

## Data storage (DVC remote)
Data and models are not stored in git: git keeps only their hashes in `dvc.lock`,
and the files themselves live in a DVC remote (see `.dvc/config`).

- `uv run dvc push` — upload data and model to the remote.
- `uv run dvc pull` — download the versions referenced by the current `dvc.lock`.

The current remote is a local folder (`C:\dvc-storage`), so it works only on this machine.

## Experiment tracking (MLflow)
Every `train` run is logged to [MLflow](https://mlflow.org/) in the `breast-cancer` experiment:
- all parameters from `params.yaml` (flattened, e.g. `pipeline.model__max_iter`);
- test metrics;
- the trained model as an MLflow Model (`model` artifact) with its signature,
  input example and Python requirements, so it can be loaded without knowing its internals.

1. Start the tracking server in a separate terminal (it runs until you stop it):
```bash
   uv run mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db
```
2. In the terminal where you run the pipeline, point the client to the server:
```powershell
   $env:MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"   # PowerShell
```
```bash
   export MLFLOW_TRACKING_URI=http://127.0.0.1:5000      # bash
```
3. Open the UI at http://127.0.0.1:5000 to browse and compare runs.

The tracking URI is environment configuration, so it is kept out of the code and `params.yaml`.
MLflow data (`mlflow.db`, `mlartifacts/`) is stored locally and ignored by git.

### Running experiments
Try other hyperparameters without editing `params.yaml` (each run is also logged to MLflow):
```bash
uv run dvc exp run -S pipeline.model__C=0.1
uv run dvc exp show          # table of experiments with params and metrics
uv run dvc exp remove --all  # delete experiments when you no longer need them
```
To keep a result, set the value in `params.yaml`, run `uv run dvc repro` and commit.

## Running tests
`uv run pytest -v` — run all tests.

Tests do not need the MLflow server: each test logs to a throwaway SQLite DB
in a temporary directory (see `tests/conftest.py`).

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
5. If the pipeline outputs changed, upload them to DVC remote storage:
```bash
   uv run dvc push
```
   Otherwise others will get `dvc.lock` with hashes but no files behind them.
6. Open a pull request into `main`.
