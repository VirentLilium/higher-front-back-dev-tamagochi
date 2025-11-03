"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик."""
        raise NotImplementedError


class Clicker(AbstractClicker):
    """Класс кликера."""

    def __init__(self, income_per_click: int, start_coins: int = 50) -> None:
        """Метод инициализации кликера, start_coins - стартовое число монет."""
        self._income_per_click = income_per_click
        self.total_coins = start_coins

    def click(self) -> None:
        """Метод клика для накапливания монет."""
        self.total_coins += self._income_per_click

    @property
    def income_per_click(self) -> int:
        """Свойство для доступа к числу монет за клик."""
        return self._income_per_click
