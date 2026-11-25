# Визуализация графа зависимостей NuGet — этап 5

## 1. Общее описание

CLI (вариант №25): граф зависимостей (DFS), фильтр,
циклы, test-mode, обратные зависимости (`--reverse-deps`).
**Этап 5** добавляет визуализацию: текст **Mermaid**,
файл **SVG** (`output/graph.svg`) и при флаге
`--ascii-tree` — дерево в терминале.

Сравнение с `dotnet list package --include-transitive`:
наш обход строится из `.nuspec` flat container и может
отличаться по версиям диапазонов и пакетам платформы.

## 2. Параметры

| Параметр | Назначение |
| --- | --- |
| `--package` | Корневой пакет |
| `--repo` | URL NuGet или путь к тестовому файлу |
| `--version` | Версия (NuGet) |
| `--test-mode` | Граф из файла `A: B C` |
| `--filter` | Исключить имена с подстрокой |
| `--reverse-deps` | Обратные зависимости (этап 4) |
| `--ascii-tree` | ASCII-дерево в терминале (этап 5) |

## 3. Запуск

```bash
chmod +x run.sh && ./run.sh
```

```bash
cd "/Users/talgat/Проекты/Конфиги"
export PYTHONPATH=.
```

Тест + Mermaid + SVG:

```bash
python3 -m src.main \
  --package A \
  --repo fixtures/repo_simple.txt \
  --version 1.0.0 \
  --test-mode
```

С ASCII-деревом:

```bash
python3 -m src.main \
  --package A \
  --repo fixtures/repo_simple.txt \
  --version 1.0.0 \
  --test-mode \
  --ascii-tree
```

Три NuGet-пакета для демонстрации (этап 5):

```bash
python3 -m src.main --package Serilog.Sinks.File \
  --repo https://api.nuget.org/v3-flatcontainer \
  --version 5.0.0 --filter System

python3 -m src.main --package NUnit \
  --repo https://api.nuget.org/v3-flatcontainer \
  --version 3.14.0 --filter Microsoft

python3 -m src.main --package AutoMapper \
  --repo https://api.nuget.org/v3-flatcontainer \
  --version 12.0.1 --ascii-tree
```

Просмотр SVG на macOS:

```bash
open output/graph.svg
```

Тесты:

```bash
python3 -m unittest discover -s tests -v
```

## 4. Пример вывода

```text
=== Mermaid ===
flowchart TD
  A["A"]
  ...
=== Изображение графа ===
output/graph.svg
```

```text
=== ASCII-дерево ===
A
├── B
│   └── D
└── C
    └── D
====================
```