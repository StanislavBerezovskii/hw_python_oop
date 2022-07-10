from typing import Dict, Type, ClassVar
from inspect import signature
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar[int] = 18
    COEFF_CALORIE_2: ClassVar[int] = 20
    COEFF_CALORIE_3: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        """Формула: (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM *
        время_тренировки_в_минутах."""

        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * (self.duration * self.COEFF_CALORIE_3))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALOR_1: ClassVar[float] = 0.035
    COEFF_CALOR_2: ClassVar[int] = 2
    COEFF_CALOR_3: ClassVar[float] = 0.029
    COEFF_CALOR_4: ClassVar[int] = 60
    height: float

    def get_spent_calories(self) -> float:
        """Формула: (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
        * время_тренировки_в_минутах."""
        return ((self.COEFF_CALOR_1 * self.weight + (self.get_mean_speed()
                ** self.COEFF_CALOR_2 // self.height) * self.COEFF_CALOR_3
                * self.weight) * (self.duration * self.COEFF_CALOR_4))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CAL_1: ClassVar[float] = 1.1
    COEFF_CAL_2: ClassVar[int] = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CAL_1)
                * self.COEFF_CAL_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_class_dict: Dict[str, Type] = {'SWM': Swimming,
                                           'RUN': Running,
                                           'WLK': SportsWalking, }

    if workout_type not in workout_class_dict.keys():
        raise KeyError(f'Ошибка: тип тренировки "{workout_type}" не обнаружен')

    if len(data) != (len(signature(workout_class_dict[workout_type])
                     .parameters)):
        raise ValueError(f'Ошибка: количество параметров '
                         f'тренировки "{workout_type}" нарушено')

    return workout_class_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
