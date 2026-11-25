#!/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH="."

NUGET="https://api.nuget.org/v3-flatcontainer"
PY="python3 -m src.main"
FIX="fixtures"

echo "=== ТЕСТ 1: Граф test-mode (этап 3) ==="
$PY --package A \
  --repo $FIX/repo_simple.txt \
  --version 1.0.0 \
  --test-mode

echo "=== ТЕСТ 2: Обратные зависимости D ==="
$PY --package D \
  --repo $FIX/repo_simple.txt \
  --version 1.0.0 \
  --test-mode \
  --reverse-deps

echo "=== ТЕСТ 3: Обратные по цепочке (пакет C) ==="
$PY --package C \
  --repo $FIX/repo_chain.txt \
  --version 1.0.0 \
  --test-mode \
  --reverse-deps

echo "=== ТЕСТ 4: Цикл + обратные (пакет B) ==="
$PY --package B \
  --repo $FIX/repo_cycle.txt \
  --version 1.0.0 \
  --test-mode \
  --reverse-deps

echo "=== ТЕСТ 5: Ошибка — нет --package ==="
set +e
$PY --repo "$NUGET" --version 5.0.0 --reverse-deps
set -e

echo "=== Юнит-тесты ==="
python3 -m unittest discover -s tests -v

echo "=== ГОТОВО ==="