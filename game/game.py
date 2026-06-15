"""Модуль с интерфейсом и реализацией игровой логики."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from copy import deepcopy
from typing import Any

from game.clicker import AbstractClicker
from game.constants import START_COINS
from game.exceptions import (
    NotEnoughFood,
    NotEnoughMedicine,
    NotEnoughMoney,
    TamagochiIsGone,
)
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
        all_medicine: list[Medicine],
    ) -> None:
        """
        Инициализирует объект игры.

        :param tamagochi: Экземпляр питомца.
        :param clicker: Экземпляр кликера.
        :param all_food: Список доступной еды.
        :param all_medicine: Список доступных лекарств.
        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Выполняет действие «работа».

        :return: Количество заработанных монет.
        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """
        Покупает еду для питомца.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """
        Покупает лекарство для питомца.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """
        Кормит питомца.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """
        Лечит питомца.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """
        Даёт питомцу отдохнуть.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """
        Играет с питомцем.

        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Возвращает текущее состояние игры.

        :return: Словарь с характеристиками питомца и игры.
        :raises NotImplementedError: Если метод не реализован в наследнике.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Возвращает список еды в инвентаре.

        :return: Список объектов еды.
        :raises NotImplementedError: Если свойство не реализовано в наследнике.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Возвращает список лекарств в инвентаре.

        :return: Список объектов лекарств.
        :raises NotImplementedError: Если свойство не реализовано в наследнике.
        """
        raise NotImplementedError


class NewGame(AbstractGame):
    """Логика игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Инициализирует новую игру.

        :param tamagochi: Экземпляр питомца.
        :param clicker: Экземпляр кликера.
        :param all_food: Список доступной еды.
        :param all_medicine: Список доступных лекарств.
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self._coins = START_COINS
        self._inventory: dict[str, list[Food] | list[Medicine]] = {
            'food': [],
            'medicine': [],
        }

    def work(self) -> int:
        """
        Выполняет действие «работа».

        :return: Количество заработанных монет.
        """
        self.clicker.click()
        new_coins = self.clicker.income_per_click
        self._coins += new_coins
        return new_coins

    def buy_food(self) -> None:
        """Покупает еду для питомца."""
        self.__buy_item(self.all_food, self.__add_food_to_inventory)

    def feed_tamagochi(self) -> None:
        """
        Кормит питомца едой из инвентаря.

        Использует первый доступный продукт и удаляет его из сумки.

        :raises NotEnoughFood: Если в инвентаре нет еды.
        """
        if not self._inventory['food']:
            raise NotEnoughFood()

        food = self._inventory['food'].pop(0)
        self.tamagochi.feed(food)

    def buy_medicine(self) -> None:
        """Покупает лекарство для питомца."""
        self.__buy_item(self.all_medicine, self.__add_medicine_to_inventory)

    def heal_tamagochi(self) -> None:
        """
        Лечит питомца лекарством из инвентаря.

        После исчерпания всех использований лекарство удаляется
        из инвентаря.

        :raises NotEnoughMedicine: Если в инвентаре нет лекарств.
        """
        if not self._inventory['medicine']:
            raise NotEnoughMedicine()

        medicine = self._inventory['medicine'][0]
        self.tamagochi.heal(medicine)
        medicine.uses += 1

        if medicine.is_empty():
            self._inventory['medicine'].pop(0)

    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть."""
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        self.tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """
        Возвращает текущее состояние игры.

        Проверяет, жив ли питомец, и добавляет количество монет
        к данным о его состоянии.

        :return: Словарь с характеристиками питомца и количеством монет.
        :raises TamagochiIsGone: Если питомец погиб.
        """
        if not self.tamagochi.is_alive():
            raise TamagochiIsGone()

        status = self.tamagochi.status
        status['coins'] = self._coins
        return status

    @property
    def food(self) -> list[Food]:
        """
        Возвращает список еды в инвентаре.

        :return: Список объектов еды.
        """
        return self._inventory['food']

    @property
    def medicine(self) -> list[Medicine]:
        """
        Возвращает список лекарств в инвентаре.

        :return: Список объектов лекарств.
        """
        return self._inventory['medicine']

    def __buy_item(
        self,
        items: list[Food] | list[Medicine],
        add_to_inventory_func: Callable[[Food | Medicine], None],
    ) -> None:
        """
        Покупает выбранный товар и добавляет его в инвентарь.

        :param items: Список доступных товаров.
        :param add_to_inventory_func: Функция добавления товара в инвентарь.
        :raises NotEnoughMoney: Если у игрока не хватает монет.
        """
        while True:
            print('Доступные товары:')

            for index, item in enumerate(items, start=1):
                print(f'{index}. {item}.')

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
        """
        Добавляет еду в инвентарь.

        :param food: Объект еды.
        """
        self._inventory['food'].append(food)

    def __add_medicine_to_inventory(self, medicine: Medicine) -> None:
        """
        Добавляет лекарство в инвентарь.

        :param medicine: Объект лекарства.
        """
        self._inventory['medicine'].append(medicine)
