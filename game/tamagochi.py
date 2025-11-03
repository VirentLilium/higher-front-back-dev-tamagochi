"""Модуль с интерфейсом и реализациями класса тамагочи."""

from abc import ABC, abstractmethod

from .models import Food, Medicine
from .exceptions import TamagochiIsGone


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи.

        :param food: объект еды для кормления.
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи.

        :param medicine: лекарство для лечения.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи.

        :return: словарь со всеми состояниями тамагочи.
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи.

        :return: True если жив, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи.

        :return: True если тамагочи болеет, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи.
        """
        raise NotImplementedError


class MyTamagochi(AbstractTamagochi):
    """Класс тамагочи."""
    MAX_HUNGER = 100
    MAX_HP = 100
    MAX_ENERGY = 100
    MAX_HAPPINESS = 100

    def __init__(self) -> None:
        """Метод инициализации тамагочи. Устанавливает стартовые показатели
        здоровья, энергии и голода."""
        self.hunger = 0  # Голод.
        self.hp = self.MAX_HP  # Здоровье.
        self.energy = self.MAX_ENERGY  # Энергия.
        self.happiness = self.MAX_HAPPINESS  # Счастье.

    def feed(self, food: Food) -> None:
        """
        Метод для кормления тамагочи.

        :param food: объект еды для кормления.
        """
        self.hunger -= food.satiety

    def play(self) -> None:
        """Метод для игры с тамагочи."""

        self.happiness += 20
        self.energy -= 10
        self.hunger += 5

    def rest(self) -> None:
        """Метод для отдыха тамагочи."""
        if self.is_sick():  # В случае болезни увеличивается только энергия.
            self.energy += 5
        else:
            self.energy += 15
            self.happiness += 5
            self.hp += 10

    def heal(self, medicine: Medicine) -> None:
        """
        Метод для лечения тамагочи.

        :param medicine: лекарство для лечения.
        """
        self.hp += medicine.heal_hp

    @property
    def status(self) -> dict[str, int]:
        """
        Свойство для доступа ко всем состояниям тамагочи.

        :return: словарь со всеми состояниями тамагочи.
        """
        tamagochi_status = {'hunger': self.hunger,
                            'hp': self.hp,
                            'energy': self.energy,
                            'happiness': self.happiness}
        return tamagochi_status

    def is_alive(self) -> bool:
        """
        Метод для проверки жив ли тамагочи.

        :return: True если жив, иначе False.
        """
        return True if self.hp > 0 else False

    def is_sick(self) -> bool:
        """
        Метод для проверки, не заболел ли тамагочи.

        :return: True если тамагочи болеет, иначе False.
        """
        tamagochi_is_sick = False

        if self.happiness < 20 or self.hp < 30 or self.hunger > 80:
            tamagochi_is_sick = True
        return tamagochi_is_sick

    def update(self) -> None:
        """
        Метод для обновления состояний тамагочи.
        Должен использоваться после каждого тика игры.
        """
        # Стандартная динамика.
        self.energy -= 5
        self.happiness -= 5
        self.hunger += 5

        # Если питомец болен, дополнительно уменьшаем показатели.
        if self.is_sick():
            self.energy -= 5
            self.happiness -= 5
            self.hp -= 5

        if not self.is_alive():
            raise TamagochiIsGone

        self._check_limits()

    def _check_limits(self) -> None:
        """
        Служебный метод для корректировки показателей,
        чтобы не было выхода за границы.
        """
        self.hunger = min(max(self.hunger, 0), self.MAX_HUNGER)
        self.hp = min(max(self.hp, 0), self.MAX_HP)
        self.energy = min(max(self.energy, 0), self.MAX_ENERGY)
        self.happiness = min(max(self.happiness, 0), self.MAX_HAPPINESS)
