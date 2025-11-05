"""Модуль с интерфейсом и реализациями класса тамагочи.

Содержит:
- AbstractTamagochi: абстрактный класс для описания логики тамагочи.
- MyTamagochi: реализация тамагочи.
- Модели: Food(еда), Medicine(лекарство).
"""

from abc import ABC, abstractmethod

from .models import Food, Medicine
from .constants import (MIN_HP, MAX_HP, MIN_ENERGY, MAX_ENERGY, MIN_HUNGER,
                        MAX_HUNGER, HUNGER_LEVEL_TO_SICK)


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи.

        Аргументы:
            food (Food): объект еды для кормления.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи.

        Аргументы:
            medicine (Medicine): лекарство для лечения.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи.

        Возвращает:
            dict[str, int]: словарь показателей состояния тамагочи.

        Исключения:
            NotImplementedError: свойство должно быть реализовано в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки, жив ли тамагочи.

        Возвращает:
            bool: True, если питомец жив, иначе False.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи.

        Возвращает:
            bool: True, если питомец болеет, иначе False.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.

        Вызывается каждый тик игры для изменения состояния питомца.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError


class MyTamagochi(AbstractTamagochi):
    """Класс тамагочи."""

    def __init__(self) -> None:
        """Метод инициализации тамагочи. Устанавливает стартовые показатели."""
        self._hunger = MIN_HUNGER  # Голод.
        self._hp = MAX_HP  # Здоровье.
        self._energy = MAX_ENERGY  # Энергия.

    def feed(self, food: Food) -> None:
        """
        Метод для кормления тамагочи.

        Аргументы:
            food (Food): еда для питомца.
        """
        self._hunger = max(MIN_HUNGER, self._hunger - food.satiety)

    def play(self) -> None:
        """Метод для игры с тамагочи."""
        self._energy = max(MIN_ENERGY, self._energy - 10)
        self._hunger = min(MAX_HUNGER, self._hunger + 5)

    def rest(self) -> None:
        """Метод для отдыха тамагочи."""
        if self.is_sick():
            self._energy = min(MAX_ENERGY, self._energy + 5)
        else:
            self._energy = min(MAX_ENERGY, self._energy + 15)

    def heal(self, medicine: Medicine) -> None:
        """
        Метод для лечения тамагочи.

        Аргументы:
            medicine (Medicine): лекарство, увеличивает здоровье.
        """
        self._hp = min(MAX_HP, self._hp + medicine.heal_hp)

    @property
    def status(self) -> dict[str, int]:
        """
        Свойство для доступа ко всем состояниям тамагочи.

        Возвращает:
            dict[str, int]: показатели питомца: голод, здоровье, энергия.
        """
        return {'hunger': self._hunger,
                'hp': self._hp,
                'energy': self._energy}

    def is_alive(self) -> bool:
        """
        Метод для проверки, жив ли тамагочи.

        Возвращает:
            bool: True, если питомец жив, иначе False.
        """
        return self._hp > MIN_HP

    def is_sick(self) -> bool:
        """Метод для проверки, не заболел ли тамагочи.

        Возвращает:
            bool: True, если питомец болен, иначе False.
        """
        return (self._hunger >= HUNGER_LEVEL_TO_SICK
                or self._energy <= MIN_ENERGY)

    def update(self) -> None:
        """Метод обновляет состояния тамагочи после каждого хода."""
        # Стандартная динамика.
        self._energy = max(MIN_ENERGY, self._energy - 5)
        self._hunger = min(MAX_HUNGER, self._hunger + 5)

        # Если питомец болен, дополнительно уменьшается здоровье.
        if self.is_sick():
            self._hp = max(MIN_HP, self._hp - 5)
