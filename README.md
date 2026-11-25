# Визуализация графа зависимостей NuGet — этап 4

## 1. Общее описание

CLI-приложение практической работы №2 (вариант №25,
Тимиров). Программа строит граф зависимостей (DFS без
рекурсии), поддерживает `--filter`, циклы и test-mode.
На **этапе 4** добавлен вывод **обратных зависимостей**:
пакеты, которые зависят от заданного `--package`
(тот же DFS по инвертированному графу).

## 2. Описание функций и настроек

| Параметр | Назначение |
| --- | --- |
| `--package` | Имя анализируемого пакета |
| `--repo` | URL репозитория или путь к тестовому файлу |
| `--test-mode` | Режим тестового репозитория |
| `--version` | Версия пакета (для NuGet) |
| `--filter` | Не учитывать пакеты с подстрокой в имени |
| `--reverse-deps` | Обратные зависимости (этап 4) |
| `--ascii-tree` | ASCII-дерево (этап 5) |

Тестовый файл: строки `A: B C` (заглавные латинские буквы).

## 3. Сборка и запуск

```bash
chmod +x run.sh && ./run.sh
```

Прямой граф (этап 3):

```bash
export PYTHONPATH="."
python3 -m src.main \
  --package A \
  --repo fixtures/repo_simple.txt \
  --version 1.0.0 \
  --test-mode
```

Обратные зависимости (этап 4):

```bash
PYTHONPATH=. python3 -m src.main \
  --package D \
  --repo fixtures/repo_simple.txt \
  --version 1.0.0 \
  --test-mode \
  --reverse-deps
```

```bash
PYTHONPATH=. python3 -m src.main \
  --package C \
  --repo fixtures/repo_chain.txt \
  --version 1.0.0 \
  --test-mode \
  --reverse-deps
```

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## 4. Примеры использования

Обратные зависимости пакета `D` (`repo_simple.txt`):

```text
=== Обратные зависимости ===
D -> B, C
B -> A
C -> A
A ->
===========================
=== Циклы ===
(нет)
=============
```

Цепочка: обратные для `C`:

```text
=== Обратные зависимости ===
C -> B
B -> A
A ->
===========================
```