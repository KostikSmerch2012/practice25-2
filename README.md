# Визуализация графа зависимостей NuGet — этап 3

## 1. Общее описание

CLI-приложение практической работы №2 (вариант №25,
Тимиров). На этапе 3 программа строит **граф зависимостей
с транзитивностью** алгоритмом **DFS без рекурсии**,
учитывает `--filter`, корректно обрабатывает циклы и
поддерживает `--test-mode` с файлом описания графа.

## 2. Описание функций и настроек

| Параметр | Назначение |
| --- | --- |
| `--package` | Имя анализируемого пакета |
| `--repo` | URL репозитория или путь к тестовому файлу |
| `--test-mode` | Режим тестового репозитория |
| `--version` | Версия пакета (для NuGet) |
| `--filter` | Не учитывать пакеты с этой подстрокой в имени |
| `--ascii-tree` | Режим ASCII-дерева (этап 5) |

Тестовый файл: строки вида `A: B C` (заглавные буквы).

## 3. Сборка и запуск

```bash
chmod +x run.sh && ./run.sh
```

```bash
export PYTHONPATH="."
python3 -m src.main \
  --package A \
  --repo fixtures/repo_simple.txt \
  --version 1.0.0 \
  --test-mode
```

```bash
PYTHONPATH=. python3 -m src.main \
  --package A \
  --repo fixtures/repo_cycle.txt \
  --version 1.0.0 \
  --test-mode
```

```bash
PYTHONPATH=. python3 -m src.main \
  --package A \
  --repo fixtures/repo_simple.txt \
  --version 1.0.0 \
  --test-mode \
  --filter B
```

```bash
PYTHONPATH=. python3 -m src.main \
  --package Serilog.Sinks.File \
  --repo "https://api.nuget.org/v3-flatcontainer" \
  --version 5.0.0 \
  --filter System
```

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## 4. Примеры использования

Алмаз `fixtures/repo_simple.txt` (пакет `A`):

```text
=== Граф зависимостей ===
A -> B, C
B -> D
C -> D
D ->
=========================
=== Циклы ===
(нет)
=============
```

Цикл `fixtures/repo_cycle.txt`:

```text
=== Граф зависимостей ===
A -> B
B -> C
C -> A
=========================
=== Циклы ===
C -> A
=============
```
