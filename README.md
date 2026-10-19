# Запуск проекта
1. `uv sync` - установить все зависимости.
2. Из корня проекта `uv run python -m mlops_testing.prepare` для подготовки данных.
3. Из корня проекта `uv run python -m mlops_testing.train` для запуска обучения и сбора метрик.
