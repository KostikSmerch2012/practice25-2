# Визуализация графа зависимостей NuGet — этап 2

## 1. Общее описание

CLI-приложение практической работы №2 (вариант №25,
Тимиров). На этапе 2 программа читает параметры
командной строки, загружает `.nuspec` заданной версии
пакета из NuGet flat container и выводит **прямые**
зависимости. Сторонние NuGet-библиотеки и менеджер
`nuget`/`dotnet` не используются — только стандартная
библиотека Python.

## 2. Описание функций и настроек

| Параметр | Назначение |
| --- | --- |
| `--package` | Имя анализируемого пакета |
| `--repo` | URL репозитория или путь к тестовому файлу |
| `--test-mode` | Режим тестового репозитория |
| `--version` | Версия пакета |
| `--ascii-tree` | Режим вывода ASCII-дерева (этап 5) |
| `--filter` | Подстрока фильтрации пакетов (этап 3) |

В обычном режиме URL `.nuspec` строится так:

```text
{repo}/{package_lower}/{version_lower}/{package_lower}.nuspec
```

Пример базы: `https://api.nuget.org/v3-flatcontainer`

## 3. Сборка и запуск

```bash
chmod +x run.sh && ./run.sh
```

```bash
export PYTHONPATH="."
python3 -m src.main \
  --package Serilog.Sinks.File \
  --repo "https://api.nuget.org/v3-flatcontainer" \
  --version 5.0.0
```

```bash
PYTHONPATH=. python3 -m src.main \
  --package A \
  --repo fixtures/repo_simple.txt \
  --version 1.0.0 \
  --test-mode
```

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## 4. Примеры использования

NuGet (прямые зависимости `Serilog.Sinks.File` 5.0.0):

```text
=== Прямые зависимости ===
Serilog 2.10.0
==========================
```

Тестовый репозиторий (пакет `A`):

```text
=== Прямые зависимости ===
B
C
==========================
```
