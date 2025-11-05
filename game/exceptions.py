"""Модуль с исключениями."""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи."""

    def __init__(self, message='Тамагочи погиб! Игра окончена!'):
        super().__init__(message)


class NotEnoughMoney(Exception):
    """Ошибка, когда не хватает монет для покупки."""

    def __init__(self, message='У вас не хватает монет на покупку товара!'):
        super().__init__(message)


class NotEnoughFood(Exception):
    """Ошибка, когда в сумке нет еды."""

    def __init__(self, message='У вас в сумке нет еды!'):
        super().__init__(message)


class NotEnoughMedicine(Exception):
    """Ошибка, когда в сумке нет лекарств."""

    def __init__(self, message='У вас в сумке нет лекарств!'):
        super().__init__(message)
