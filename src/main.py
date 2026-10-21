"""Точка входа CLI — этап 1 (конфигурация)."""

import sys

from src.config import load_config, print_config, success_code


def main(argv=None):
    """Читает параметры CLI и выводит их на экран."""
    args = load_config(argv)
    print_config(args)
    return success_code()


if __name__ == "__main__":
    sys.exit(main())
