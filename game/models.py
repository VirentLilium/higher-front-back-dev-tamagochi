"""Модуль с моделями."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """
    Модель еды.

    :param name: Название продукта.
    :param satiety: Количество единиц сытости.
    :param price: Стоимость продукта.
    """

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта еды.

        :return: Информация о продукте.
        """
        return (
            f'{self.name} стоимость: {self.price}, '
            f'утоляет голод на {self.satiety} единиц.'
        )


@dataclass
class Medicine:
    """
    Модель лекарства.

    :param name: Название лекарства.
    :param price: Стоимость лекарства.
    :param heal_hp: Количество восстанавливаемого здоровья.
    :param number_of_uses: Максимальное количество использований.
    :param uses: Текущее количество использований.
    """

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """
        Проверяет, осталось ли еще лекарство.

        :return: True, если количество использований исчерпано,
            иначе False.
        """
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта лекарства.

        :return: Информация о лекарстве.
        """
        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, использований: '
            f'{self.number_of_uses - self.uses}/{self.number_of_uses}.'
        )
