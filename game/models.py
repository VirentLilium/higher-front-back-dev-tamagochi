"""Модуль с моделями."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """
    Модель объекта еды.

    Атрибуты:
        name (str): наименование.
        satiety (int): утоляет голод на указанное количество единиц.
        price (int): стоимость продукта.
    """

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта."""
        return (
            f"{self.name} стоимость: {self.price}, "
            f"утоляет голод на {self.satiety} единиц."
        )


@dataclass
class Medicine:
    """
    Модель объекта лекарства.

    Атрибуты:
        name (str): наименование.
        price (int): стоимость.
        heal_hp (int): сколько лечит HP.
        number_of_uses (int): максимальное количество применений.
        uses (int): текущее количество применений (по умолчанию 0).
    """

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """
        Проверяет, осталось ли еще лекарство.

        Возвращает:
            bool: True, если лекарство закончилось, иначе False.
        """
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта."""
        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, использований: '
            f'{self.number_of_uses - self.uses}/{self.number_of_uses}.'
        )
