"""Модуль с интерфейсом и реализацией класса тамагочи."""

from abc import ABC, abstractmethod

from .constants import (
    HUNGER_LEVEL_TO_SICK,
    MAX_ENERGY,
    MAX_HP,
    MAX_HUNGER,
    MIN_ENERGY,
    MIN_HP,
    MIN_HUNGER,
)
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Кормит тамагочи.

        :param food: Объект еды для кормления.
        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """
        Играет с тамагочи.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """
        Даёт тамагочи отдохнуть.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Лечит тамагочи.

        :param medicine: Лекарство для восстановления здоровья.
        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Возвращает текущее состояние тамагочи.

        :return: Словарь с показателями голода, здоровья и энергии.
        :raises NotImplementedError: Если свойство не реализовано в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Проверяет, жив ли тамагочи.

        :return: True, если питомец жив, иначе False.
        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Проверяет, болеет ли тамагочи.

        :return: True, если питомец болеет, иначе False.
        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Обновляет состояние тамагочи после хода.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError


class MyTamagochi(AbstractTamagochi):
    """Реализация логики тамагочи."""

    def __init__(self) -> None:
        """
        Инициализирует тамагочи.

        Начальные значения:
        - голод минимальный;
        - здоровье максимальное;
        - энергия максимальная.
        """
        self._hunger = MIN_HUNGER
        self._hp = MAX_HP
        self._energy = MAX_ENERGY

    def feed(self, food: Food) -> None:
        """
        Кормит тамагочи и уменьшает уровень голода.

        :param food: Объект еды для кормления.
        """
        self._hunger = max(MIN_HUNGER, self._hunger - food.satiety)

    def play(self) -> None:
        """
        Играет с тамагочи.

        Игра уменьшает энергию питомца и повышает уровень голода.
        """
        self._energy = max(MIN_ENERGY, self._energy - 10)
        self._hunger = min(MAX_HUNGER, self._hunger + 5)

    def rest(self) -> None:
        """
        Даёт тамагочи отдохнуть.

        Если питомец болеет, отдых восстанавливает меньше энергии.
        """
        if self.is_sick():
            self._energy = min(MAX_ENERGY, self._energy + 5)
        else:
            self._energy = min(MAX_ENERGY, self._energy + 15)

    def heal(self, medicine: Medicine) -> None:
        """
        Лечит тамагочи и восстанавливает здоровье.

        :param medicine: Лекарство для восстановления здоровья.
        """
        self._hp = min(MAX_HP, self._hp + medicine.heal_hp)

    @property
    def status(self) -> dict[str, int]:
        """
        Возвращает текущее состояние тамагочи.

        :return: Словарь с показателями голода, здоровья и энергии.
        """
        return {
            'hunger': self._hunger,
            'hp': self._hp,
            'energy': self._energy
        }

    def is_alive(self) -> bool:
        """
        Проверяет, жив ли тамагочи.

        :return: True, если здоровье питомца выше минимального значения.
        """
        return self._hp > MIN_HP

    def is_sick(self) -> bool:
        """
        Проверяет, болеет ли тамагочи.

        :return: True, если голод слишком высокий или энергия закончилась.
        """
        return (self._hunger >= HUNGER_LEVEL_TO_SICK
                or self._energy <= MIN_ENERGY)

    def update(self) -> None:
        """
        Обновляет состояние тамагочи после хода.

        После каждого хода питомец теряет энергию и становится голоднее.
        Если питомец болеет, дополнительно уменьшается здоровье.
        """
        self._energy = max(MIN_ENERGY, self._energy - 5)
        self._hunger = min(MAX_HUNGER, self._hunger + 5)

        if self.is_sick():
            self._hp = max(MIN_HP, self._hp - 5)
