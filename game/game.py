"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from typing import Any

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine
from .exceptions import NotEnoughMoney


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

        :param tamagochi: экземпляр тамагочи.
        :param clicker: экземпляр кликера.
        :param all_food: все доступные варианты еды.
        :param all_medicine: все доступные варианты лекарств.
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа.

        :return: количество заработанных монет.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи.

        :return: словарь со всеми характеристиками тамагочи.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой.

        :return: список с имеющимися (купленными) объектами еды.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами.

        :return: список с имеющимися (купленными) объектами лекарств.
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

        :param tamagochi: экземпляр тамагочи.
        :param clicker: экземпляр кликера.
        :param all_food: все доступные варианты еды.
        :param all_medicine: все доступные варианты лекарств.
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food  # Каталог всех продуктов.
        self.all_medicine = all_medicine  # Каталог всех лекарств.
        self._food_inventory: list[Food] = []  # Сумка с купленными продуктами.
        # Сумка с купленными лекарствами.
        self._medicine_inventory: list[Medicine] = []

    def work(self) -> int:
        """
        Метод для логики действия "работа.

        :return: количество заработанных монет.
        """
        self.clicker.click()
        return self.clicker.income_per_click

    def buy_food(self) -> None:
        """ Метод для покупки еды."""
        while True:
            print('Доступные продукты:')
            for i, food in enumerate(self.all_food, start=1):
                print(f'{i}. {food}.')
            try:
                choice = int(input('Выберите номер продукта для покупки')) - 1
                if choice < 0 or choice >= len(self.all_food):
                    raise ValueError('Выберите номер продукта из предложенных')

                food_to_buy = self.all_food[choice]

                if self.clicker.total_coins < food_to_buy.price:
                    raise NotEnoughMoney

                self.clicker.total_coins -= food_to_buy.price
                self._food_inventory.append(food_to_buy)
                print(f'Вы купили {food_to_buy.name}'
                      f'за {food_to_buy.price} монет.')
                break
            except ValueError as e:
                print(e)

    def buy_medicine(self) -> None:
        """Метод для покупки лекарства."""
        while True:
            print('Доступные продукты:')
            for i, medicine in enumerate(self.all_medicine, start=1):
                print(f'{i}. {medicine}.')
            try:
                choice = int(input('Выберите номер лекарства для покупки')) - 1
                if choice < 0 or choice >= len(self.all_medicine):
                    raise ValueError(
                        'Выберите номер лекарства из предложенных')

                medicine_to_buy = self.all_medicine[choice]

                if self.clicker.total_coins < medicine_to_buy.price:
                    raise NotEnoughMoney

                self.clicker.total_coins -= medicine_to_buy.price
                self._medicine_inventory.append(medicine_to_buy)
                print(f'Вы купили {medicine_to_buy.name} за'
                      f'{medicine_to_buy.price} монет.')
                break
            except ValueError as e:
                print(e)

    def feed_tamagochi(self) -> None:
        """Метод для кормления тамагочи."""
        raise NotImplementedError

    def heal_tamagochi(self) -> None:
        """Метод для лечения тамагочи."""
        raise NotImplementedError

    def rest_tamagochi(self):
        """Метод для отдыха тамагочи."""
        raise NotImplementedError

    def play_with_tamagochi(self):
        """Метод для игры с тамагочи."""
        raise NotImplementedError

    def get_status(self) -> dict[str, Any]:
        """
        Метод для получения статуса (всех характеристик) тамагочи.

        :return: словарь со всеми характеристиками тамагочи.
        """
        status = self.tamagochi.status
        status['coins'] = self.clicker.total_coins
        return status

    @property
    def food(self) -> list[Food]:
        """
        Свойство для доступа к сумке с едой.

        :return: список с имеющимися (купленными) объектами еды.
        """
        return self._food_inventory

    @property
    def medicine(self) -> list[Medicine]:
        """
        Свойство для доступа к сумке с лекарствами.

        :return: список с имеющимися (купленными) объектами лекарств.
        """
        return self._medicine_inventory
