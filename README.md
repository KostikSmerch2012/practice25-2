# Визуализация графа зависимостей NuGet — этап 1

## 1. Общее описание

Минимальный CLI-прототип практической работы №2
(вариант №25, Тимиров). На этапе 1 приложение читает
параметры командной строки, проверяет их и выводит в
формате ключ-значение. Сбор зависимостей NuGet и
визуализация — на следующих этапах.

## 2. Описание функций и настроек

| Параметр | Назначение |
| --- | --- |
| `--package` | Имя анализируемого пакета |
| `--repo` | URL репозитория или путь к тестовому файлу |
| `--test-mode` | Режим тестового репозитория |
| `--version` | Версия пакета |
| `--ascii-tree` | Режим вывода ASCII-дерева |
| `--filter` | Подстрока для фильтрации пакетов |

## 3. Сборка и запуск

```bash
chmod +x run.sh && ./run.sh
```

```bash
export PYTHONPATH="."
python3 -m src.main \
  --package Serilog.Sinks.File \
  --repo "https://api.nuget.org/v3-flatcontainer" \
  --version 5.0.0 \
  --ascii-tree \
  --filter System
```

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## 4. Примеры использования

```text
=== Параметры конфигурации ===
package=Serilog.Sinks.File
repo=https://api.nuget.org/v3-flatcontainer
test_mode=False
version=5.0.0
ascii_tree=True
filter=System
================================
```
