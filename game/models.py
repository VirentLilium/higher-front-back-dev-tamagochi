"""Модуль с моделями."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """Модель объекта еды."""

    name: str  # Наименование.
    satiety: int  # На сколько единиц утоляет голод.
    price: int  # Стоимость.

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта."""
        return (
            f"{self.name} стоимость: {self.price}, "
            f"утоляет голод на {self.satiety} единиц."
        )


@dataclass
class Medicine:
    """Модель объекта лекарства."""

    name: str  # Наименование.
    price: int  # Стоимость.
    heal_hp: int  # Сколько лечит HP.
    number_of_uses: int  # Максимальное количество применений.
    uses: int = 0  # Текущее количество применений.

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
