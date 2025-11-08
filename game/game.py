"""Модуль с интерфейсом и реализацией класса игры.

Содержит классы, реализующие логику игры 'Тамагочи':
    - AbstractGame: интерфейс игры.
    - NewGame: реализация логики игры.
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any

from game.clicker import AbstractClicker
from game.constants import START_COINS
from game.exceptions import (NotEnoughMoney, NotEnoughFood, NotEnoughMedicine,
                             TamagochiIsGone)
from game.models import Food, Medicine
from game.tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры.

        Аргументы:
            tamagochi (AbstractTamagochi): экземпляр класса тамагочи.
            clicker (AbstractClicker): экземпляр класса кликера.
            all_food (list[Food]): список вариантов еды.
            all_medicine (list[Medicine]): список вариантов лекарств.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия 'работа'.
        Позволяет зарабатывать монеты.

        Возвращает:
            int: количество заработанных монет.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """
        Абстрактный метод для покупки еды для питомца.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """
        Абстрактный метод для покупки лекарства для питомца.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """
        Абстрактный метод для кормления тамагочи.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """
        Абстрактный метод для лечения тамагочи.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """
        Абстрактный метод для отдыха тамагочи.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """
        Абстрактный метод для игры с тамагочи.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения характеристик тамагочи и игры.

        Возвращает:
            dict[str, Any]: словарь с характеристиками тамагочи и игры.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой.

        Возвращает:
            list[Food]: список с имеющимися объектами еды.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами.

        Возвращает:
            list[Medicine]: список с имеющимися объектами лекарств.

        Исключения:
            NotImplementedError: метод должен быть реализован в наследнике.
        """
        raise NotImplementedError


class NewGame(AbstractGame):
    """Логика игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Метод инициализации класса игры.

        Аргументы:
            tamagochi (AbstractTamagochi): экземпляр питомца.
            clicker (AbstractClicker): экземпляр кликера.
            all_food (list[Food]): каталог всех продуктов.
            all_medicine (list[Medicine]): каталог всех лекарств.

        Атрибуты экземпляра:
            self._coins (int): кошелек игрока, стартовое значение START_COINS.
            self._inventory (dict[str, list]): сумка с купленными продуктами.
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self._coins = START_COINS
        self._inventory: dict[str, list] = {
            'food': [],
            'medicine': []}

    def work(self) -> int:
        """
        Метод для логики действия 'работа'.

        Возвращает:
            int: количество заработанных монет.
        """
        self.clicker.click()
        new_coins = self.clicker.income_per_click
        self._coins += new_coins
        return new_coins

    def buy_food(self) -> None:
        """Метод для покупки еды."""
        self.__buy_item(self.all_food, self.__add_food_to_inventory)

    def feed_tamagochi(self) -> None:
        """
        Метод для кормления тамагочи.

        Берём первый элемент и удаляем из списка.
        """
        if not self._inventory['food']:
            raise NotEnoughFood()

        food = self._inventory['food'].pop(0)
        self.tamagochi.feed(food)

    def buy_medicine(self) -> None:
        """Метод для покупки лекарства."""
        self.__buy_item(self.all_medicine, self.__add_medicine_to_inventory)

    def heal_tamagochi(self) -> None:
        """
        Метод для лечения тамагочи.

        Если лекарство использовано полностью, то удаляем из инвентаря.
        """
        if not self._inventory['medicine']:
            raise NotEnoughMedicine()

        medicine = self._inventory['medicine'][0]
        self.tamagochi.heal(medicine)
        medicine.uses += 1

        if medicine.is_empty():
            self._inventory['medicine'].pop(0)

    def rest_tamagochi(self):
        """Метод для отдыха тамагочи."""
        self.tamagochi.rest()

    def play_with_tamagochi(self):
        """Метод для игры с тамагочи."""
        self.tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """
        Метод для получения характеристик тамагочи,
        количества монет в кошельке игрока,
        а также для обработки смерти питомца.

        Возвращает:
            dict[str, Any]: словарь со всеми характеристиками тамагочи и игры.

        Исключения:
            TamagochiIsGone: тамагочи погиб.
        """
        if not self.tamagochi.is_alive():
            raise TamagochiIsGone()

        status = self.tamagochi.status
        status['coins'] = self._coins
        return status

    @property
    def food(self) -> list[Food]:
        """
        Свойство для доступа к сумке с едой.

        Возвращает:
            list[Food]: список с имеющимися объектами еды.
        """
        return self._inventory['food']

    @property
    def medicine(self) -> list[Medicine]:
        """
        Свойство для доступа к сумке с лекарствами.

        Возвращает:
            list[Medicine]: список с имеющимися объектами лекарств.
        """
        return self._inventory['medicine']

    def __buy_item(self, items: list, add_to_inventory_func) -> None:
        """
        Универсальный метод для покупки еды или лекарства.

        Игрок выбирает товар из списка.

        Исключения:
            NotEnoughMoney: у пользователя не хватает денег для покупки.
        """
        while True:
            print('Доступные товары:')
            for i, item in enumerate(items, start=1):
                print(f'{i}. {item}.')
            try:
                choice = int(input('Выберите номер товара для покупки.')) - 1
                if choice < 0 or choice >= len(items):
                    raise ValueError

                item = items[choice]

                if self._coins < item.price:
                    raise NotEnoughMoney()

                self._coins -= item.price

                if items is self.all_medicine:
                    add_to_inventory_func(deepcopy(item))
                else:
                    add_to_inventory_func(item)

                print(f'Вы купили {item.name} за {item.price} монет.')
                break

            except ValueError:
                print('Пожалуйста, выберите номер товара из списка.')

    def __add_food_to_inventory(self, food: Food) -> None:
        """Добавляет еду в инвентарь."""
        self._inventory['food'].append(food)

    def __add_medicine_to_inventory(self, medicine: Medicine) -> None:
        """Добавляет лекарство в инвентарь."""
        self._inventory['medicine'].append(medicine)
