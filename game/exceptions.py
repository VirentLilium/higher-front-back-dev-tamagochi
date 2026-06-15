"""Модуль с пользовательскими исключениями."""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи."""

    def __init__(
        self,
        message: str = 'Тамагочи погиб! Игра окончена!',
    ) -> None:
        """
        Инициализирует исключение гибели питомца.

        :param message: Текст сообщения об ошибке.
        """
        super().__init__(message)


class NotEnoughError(Exception):
    """Базовое исключение недостатка ресурсов."""


class NotEnoughMoney(NotEnoughError):
    """Ошибка, когда не хватает монет для покупки."""

    def __init__(
        self,
        message: str = 'У вас не хватает монет на покупку товара!',
    ) -> None:
        """
        Инициализирует исключение недостатка монет.

        :param message: Текст сообщения об ошибке.
        """
        super().__init__(message)


class NotEnoughFood(NotEnoughError):
    """Ошибка, когда в сумке нет еды."""

    def __init__(
        self,
        message: str = 'У вас в сумке нет еды!',
    ) -> None:
        """
        Инициализирует исключение отсутствия еды.

        :param message: Текст сообщения об ошибке.
        """
        super().__init__(message)


class NotEnoughMedicine(NotEnoughError):
    """Ошибка, когда в сумке нет лекарств."""

    def __init__(
        self,
        message: str = 'У вас в сумке нет лекарств!',
    ) -> None:
        """
        Инициализирует исключение отсутствия лекарств.

        :param message: Текст сообщения об ошибке.
        """
        super().__init__(message)
