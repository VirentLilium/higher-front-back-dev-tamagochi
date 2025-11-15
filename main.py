import os

from game.models import Food, Medicine
from game.tamagochi import MyTamagochi
from game.clicker import Clicker
from game.constants import STATUS_TEMPLATE, TAMAGOCHI_IS_SICK, PLAYER_ACTIONS
from game.game import NewGame
from game.exceptions import (NotEnoughError, TamagochiIsGone)


def main():
    """Запускаем игру."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = MyTamagochi()

    clicker = Clicker(10, 20)

    game = NewGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        print(f"{output}\n"
              f"Сумка с едой: {game.food}\n"
              f"Сумка с лекарствами: {game.medicine}")

        try:
            print(STATUS_TEMPLATE.format(**game.get_status()))

            if game.tamagochi.is_sick():
                print(TAMAGOCHI_IS_SICK)

            print(PLAYER_ACTIONS)

            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                    game.tamagochi.update()
                case "2":
                    game.buy_food()
                case "3":
                    game.buy_medicine()
                case "4":
                    game.feed_tamagochi()
                case "5":
                    game.heal_tamagochi()
                case "6":
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case "7":
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case "0":
                    break
                case _:
                    output = "Неверная команда"

        except NotEnoughError as e:
            print(e)
            input("Нажмите Enter для продолжения игры.")

        except TamagochiIsGone as e:
            print(e)
            input("Нажмите Enter для выхода из игры.")
            break

        os.system('clear')


if __name__ == "__main__":
    main()
