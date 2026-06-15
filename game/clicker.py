"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """
        Инициализирует объект кликера.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """
        Выполняет клик и обновляет доход.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """
        Возвращает доход за последний клик.

        :return: Количество заработанных монет.
        :raises NotImplementedError: Если свойство не реализовано в наследнике.
        """
        raise NotImplementedError


class Clicker(AbstractClicker):
    """Реализация кликера со случайным доходом за клик."""

    def __init__(self, min_coins: int, max_coins: int) -> None:
        """
        Инициализирует кликер.

        :param min_coins: Минимальное количество монет за клик.
        :param max_coins: Максимальное количество монет за клик.
        """
        self._min_coins = min_coins
        self._max_coins = max_coins
        self._income_per_click = 0

    @property
    def income_per_click(self) -> int:
        """
        Возвращает доход за последний клик.

        :return: Количество заработанных монет.
        """
        return self._income_per_click

    def click(self) -> None:
        """Генерирует случайный доход за один клик."""
        self._income_per_click = randint(
            self._min_coins,
            self._max_coins,
        )
