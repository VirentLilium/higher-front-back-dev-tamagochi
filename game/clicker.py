"""Модуль с интерфейсом и реализацией кликера.

Содержит:
    - AbstractClicker: интерфейс кликера.
    - Clicker: реализация кликера со случайным доходом за клик.
"""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError


class Clicker(AbstractClicker):
    """Класс кликера. Реализация кликера со случайным доходом за клик."""

    def __init__(self, min_coins: int, max_coins: int) -> None:
        """Инициализация кликера.

        Аргументы:
            min_coins (int): минимальное количество монет за клик.
            max_coins (int): максимальное количество монет за клик.
        """
        self._min_coins = min_coins
        self._max_coins = max_coins
        self._income_per_click = 0

    @property
    def income_per_click(self) -> int:
        """Возвращает количество заработанных монет за последний клик."""
        return self._income_per_click

    def click(self) -> None:
        """Выбирает случайное количество монет за клик."""
        self._income_per_click = randint(self._min_coins, self._max_coins)
