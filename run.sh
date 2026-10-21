#!/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH="."

NUGET="https://api.nuget.org/v3-flatcontainer"
PY="python3 -m src.main"

echo "=== ТЕСТ 1: Ошибка — нет --package ==="
set +e
$PY --repo "$NUGET" --version "5.0.0"
set -e

echo "=== ТЕСТ 2: Ошибка — нет --repo ==="
set +e
$PY --package Serilog --version "5.0.0"
set -e

echo "=== ТЕСТ 3: Ошибка — нет --version ==="
set +e
$PY --package Serilog --repo "$NUGET"
set -e

echo "=== ТЕСТ 4: Ошибка — путь без --test-mode ==="
set +e
$PY --package Serilog --repo fixtures/repo_simple.txt \
  --version 1.0.0
set -e

echo "=== ТЕСТ 5: Ошибка — нет файла test-mode ==="
set +e
$PY --package A --repo missing.txt \
  --version 1.0.0 --test-mode
set -e

echo "=== ТЕСТ 6: Успех — NuGet URL, все параметры ==="
$PY --package Serilog.Sinks.File \
  --repo "$NUGET" \
  --version 5.0.0 \
  --ascii-tree \
  --filter System

echo "=== ТЕСТ 7: Успех — тестовый репозиторий ==="
$PY --package A \
  --repo fixtures/repo_simple.txt \
  --version 1.0.0 \
  --test-mode

echo "=== Юнит-тесты ==="
python3 -m unittest discover -s tests -v

echo "=== ГОТОВО ==="
