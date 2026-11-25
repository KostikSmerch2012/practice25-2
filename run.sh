#!/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH="."

NUGET="https://api.nuget.org/v3-flatcontainer"
PY="python3 -m src.main"
FIX="fixtures"

echo "=== ТЕСТ 1: Mermaid + SVG (test-mode) ==="
$PY --package A \
  --repo $FIX/repo_simple.txt \
  --version 1.0.0 \
  --test-mode

echo "=== ТЕСТ 2: ASCII-дерево ==="
$PY --package A \
  --repo $FIX/repo_simple.txt \
  --version 1.0.0 \
  --test-mode \
  --ascii-tree

echo "=== ТЕСТ 3: NuGet Serilog.Sinks.File ==="
$PY --package Serilog.Sinks.File \
  --repo "$NUGET" \
  --version 5.0.0 \
  --filter System

echo "=== ТЕСТ 4: NuGet NUnit ==="
$PY --package NUnit \
  --repo "$NUGET" \
  --version 3.14.0 \
  --filter Microsoft

echo "=== ТЕСТ 5: NuGet AutoMapper + дерево ==="
$PY --package AutoMapper \
  --repo "$NUGET" \
  --version 12.0.1 \
  --ascii-tree

echo "=== Юнит-тесты ==="
python3 -m unittest discover -s tests -v

echo "=== ГОТОВО ==="
echo "SVG: output/graph.svg  MMD: output/graph.mmd"