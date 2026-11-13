#!/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH="."

NUGET="https://api.nuget.org/v3-flatcontainer"
PY="python3 -m src.main"
FIX="fixtures"

echo "=== ТЕСТ 1: Ошибка — нет --package ==="
set +e
$PY --repo "$NUGET" --version "5.0.0"
set -e

echo "=== ТЕСТ 2: Ошибка — путь без --test-mode ==="
set +e
$PY --package Serilog --repo $FIX/repo_simple.txt \
  --version 1.0.0
set -e

echo "=== ТЕСТ 3: Алмаз без циклов ==="
$PY --package A \
  --repo $FIX/repo_simple.txt \
  --version 1.0.0 \
  --test-mode

echo "=== ТЕСТ 4: Цепочка транзитивности ==="
$PY --package A \
  --repo $FIX/repo_chain.txt \
  --version 1.0.0 \
  --test-mode

echo "=== ТЕСТ 5: Циклические зависимости ==="
$PY --package A \
  --repo $FIX/repo_cycle.txt \
  --version 1.0.0 \
  --test-mode

echo "=== ТЕСТ 6: Фильтр исключает B ==="
$PY --package A \
  --repo $FIX/repo_simple.txt \
  --version 1.0.0 \
  --test-mode \
  --filter B

echo "=== ТЕСТ 7: NuGet граф Serilog.Sinks.File ==="
$PY --package Serilog.Sinks.File \
  --repo "$NUGET" \
  --version 5.0.0 \
  --filter System

echo "=== Юнит-тесты ==="
python3 -m unittest discover -s tests -v

echo "=== ГОТОВО ==="
