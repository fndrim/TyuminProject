import pygame
import os
import math
from abc import ABC, abstractmethod
from collections import deque

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("High jump")

# Шрифт для текста
font = pygame.font.Font(None, 36)

class GameObject(ABC):
    def __init__(self, appearance, x, y):
        self.appearance = appearance  # Внешний вид или название объекта
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, screen):
        """Отрисовка объекта на экране."""
        pass

    @abstractmethod
    def update(self):
        """Обновление состояния объекта (например, перемещение)."""
        pass

    def interact(self, other, screen):
        """Взаимодействие с другим объектом."""
        pass

    def is_off_screen(self):
        """Проверка, находится ли объект за пределами экрана."""
        return (
            self.x < 0 or self.x > SCREEN_WIDTH or
            self.y < 0 or self.y > SCREEN_HEIGHT
        )

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return f"{self.appearance} (x: {self.x}, y: {self.y})"

# Класс Локация
class Location:
    # Статическое поле для хранения количества загруженных фонов
    total_backgrounds_loaded = 0

    # Статическое поле для хранения текущего уровня игры
    current_level = 1

    def __init__(self):
        self.backgrounds = deque()  # deque для динамической структуры данных
        self.current_background_index = 0

    def add_background(self, background_path):
        """Добавляет новый фон в список."""
        try:
            if os.path.exists(background_path):
                background = pygame.image.load(background_path).convert()
                self.backgrounds.append(background)
                Location.total_backgrounds_loaded += 1  # Увеличиваем счетчик загруженных фонов
                message = f"Фон {background_path} успешно загружен!"
                draw_text(screen, message, 50, 350)
            else:
                raise FileNotFoundError(f"Файл {background_path} не найден.")
        except Exception as e:
            print(f"Ошибка при загрузке фона: {e}")
            draw_text(screen, f"Ошибка: {e}", 50, 350)

    def change_background(self, character, screen):
        """Меняет фон в зависимости от счета персонажа."""
        try:
            if character.score >= 2000 and len(self.backgrounds) > 2:
                self.current_background_index = 2
            elif character.score >= 1000 and len(self.backgrounds) > 1:
                self.current_background_index = 1
            else:
                self.current_background_index = 0
            message = f"Фон изменен на {self.current_background_index + 1}!"
            draw_text(screen, message, 50, 400)
        except Exception as e:
            print(f"Ошибка при изменении фона: {e}")

    def draw_background(self, screen):
        """Отрисовывает текущий фон на экране."""
        try:
            if self.backgrounds:
                screen.blit(self.backgrounds[self.current_background_index], (0, 0))
        except Exception as e:
            print(f"Ошибка при отрисовке фона: {e}")

    # Статический метод для получения информации о загруженных фонах
    @staticmethod
    def get_background_info():
        return f"Всего загружено фонов: {Location.total_backgrounds_loaded}"

    # Статический метод для изменения уровня игры
    @staticmethod
    def set_level(new_level):
        try:
            if new_level > 0:
                Location.current_level = new_level
                return f"Уровень изменен на {new_level}"
            else:
                raise ValueError("Уровень должен быть больше 0.")
        except Exception as e:
            return f"Ошибка: {e}"

    # Статический метод для получения текущего уровня
    @staticmethod
    def get_current_level():
        return f"Текущий уровень: {Location.current_level}"

    # Класс Персонаж
    class Character(GameObject):
        def __init__(self, appearance, location):
            super().__init__(appearance, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Устанавливаем начальные координаты
            self.score = 0
            self.bullets = deque()
            self.location = location

        def shoot(self, target, screen):
            """Стрельба по цели."""
            try:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = self.Bullet(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, target_x, target_y)
                self.bullets.append(bullet)
                message = f"{self.appearance} стреляет в направлении ({target_x}, {target_y})!"
                draw_text(screen, message, 50, 100)
                if isinstance(target, Location.Monster):
                    target.die(screen)
            except Exception as e:
                print(f"Ошибка при стрельбе: {e}")

        def update_bullets(self, screen, monsters):
            """Обновление состояния пуль."""
            try:
                for bullet in list(self.bullets):  # list для итерации по копии
                    bullet.update()
                    bullet.draw(screen)
                    if bullet.is_off_screen():
                        self.bullets.remove(bullet)
                    for monster in monsters:
                        if math.hypot(bullet.x - monster.x, bullet.y - monster.y) < 20:
                            monster.die(screen)
                            self.bullets.remove(bullet)
            except Exception as e:
                print(f"Ошибка при обновлении пуль: {e}")

        def jump(self, platform, screen):
            """Прыжок на платформу."""
            try:
                message = f"{self.appearance} прыгает на {platform.appearance}!"
                draw_text(screen, message, 50, 150)
                platform.interact(self, screen)
            except Exception as e:
                print(f"Ошибка при прыжке: {e}")

        def draw(self, screen):
            """Отрисовка персонажа."""
            try:
                pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 20)  # Отрисовка персонажа
            except Exception as e:
                print(f"Ошибка при отрисовке персонажа: {e}")

        def update(self):
            """Обновление состояния персонажа."""
            pass  # Логика обновления персонажа (можно добавить позже)

        def increase_score(self, points):
            """Увеличение счета персонажа."""
            try:
                if points > 0:
                    self.score += points
                    print(f"Счет увеличен на {points}. Текущий счет: {self.score}")
                else:
                    raise ValueError("Количество очков должно быть положительным.")
            except Exception as e:
                print(f"Ошибка при увеличении счета: {e}")

        def reset_score(self):
            """Сброс счета персонажа."""
            try:
                self.score = 0
                print("Счет сброшен.")
            except Exception as e:
                print(f"Ошибка при сбросе счета: {e}")

        def __add__(self, other):
            """Перегрузка оператора + для увеличения счета."""
            if isinstance(other, int):
                self.score += other
            return self

        def __str__(self):
            """Перегрузка оператора str() для вывода информации о персонаже."""
            return f"Персонаж: {self.appearance}, Счет: {self.score}"

        def __eq__(self, other):
            """Перегрузка оператора == для сравнения персонажей по счету."""
            if isinstance(other, Location.Character):  # Используем полное имя класса
                return self.score == other.score
            return False

        # Класс Пуля
        class Bullet(GameObject):
            def __init__(self, x, y, target_x, target_y):
                self.x = x
                self.y = y
                self.speed = 10
                angle = math.atan2(target_y - y, target_x - x)
                self.dx = math.cos(angle) * self.speed
                self.dy = math.sin(angle) * self.speed

            def update(self):
                self.x += self.dx
                self.y += self.dy

            def draw(self, screen):
                pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)

            def is_off_screen(self):
                return self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT

    # Класс Платформа (вложен в Location)
    class Platform(GameObject):
        def __init__(self, appearance, platform_type):
            self.appearance = appearance
            self.platform_type = platform_type

        def interact(self, character, screen):
            try:
                if self.platform_type == "normal":
                    message = f"{character.appearance} отпрыгивает выше!"
                    draw_text(screen, message, 50, 200)
                    character.increase_score(100)  # Используем метод increase_score
                elif self.platform_type == "broken":
                    message = f"{character.appearance} падает вниз, так как платформа сломалась!"
                    draw_text(screen, message, 50, 250)
                    character.increase_score(-50)  # Используем метод increase_score
                elif self.platform_type == "moving":
                    message = f"{character.appearance} отпрыгивает от движущейся платформы!"
                    draw_text(screen, message, 50, 300)
                    character.increase_score(150)  # Используем метод increase_score
            except Exception as e:
                print(f"Ошибка при взаимодействии с платформой: {e}")

        def draw(self, screen):
            pass  # Отрисовка платформы (можно добавить позже)

        def update(self):
            pass  # Обновление платформы (можно добавить позже)

    # Класс Монстр
    class Monster(GameObject):
        def __init__(self, appearance, x, y):
            self.appearance = appearance
            self.x = x
            self.y = y

        def die(self, screen):
            try:
                message = f"{self.appearance} погибает и исчезает!"
                draw_text(screen, message, 50, 450)
            except Exception as e:
                print(f"Ошибка при уничтожении монстра: {e}")

        def draw(self, screen):
            pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 20)

        def update(self):
            pass  # Обновление монстра (можно добавить позже)

# Функция для отрисовки текста на экране
def draw_text(screen, text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

# Взаимодействия классов
if __name__ == "__main__":
    # Создание локации
    location = Location()

    # Создание персонажа
    hero = location.Character("Герой", location)  # Исправлено: передаем appearance и location

    # Создаем платформы
    normal_platform = location.Platform("Обычная платформа", "normal")
    broken_platform = location.Platform("Сломанная платформа", "broken")
    moving_platform = location.Platform("Движущаяся платформы", "moving")

    # Загружаем фоны
    try:
        location.add_background("background1.png")  # Фон для счета < 1000
        location.add_background("background2.png")  # Фон для счета >= 1000
        location.add_background("background3.png")  # Фон для счета >= 2000
    except Exception as e:
        print(f"Ошибка при загрузке фонов: {e}")

    # Создание монстров
    monsters = [location.Monster("Монстр 1", 200, 200), location.Monster("Монстр 2", 800, 800)]

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                hero.shoot(monsters[0], screen)

        # Очистка экрана
        screen.fill((0, 0, 0))  # Черный фон

        # Отрисовка текущего фона
        location.draw_background(screen)

        # Пример взаимодействия
        hero.jump(normal_platform, screen)
        hero.jump(broken_platform, screen)
        hero.jump(moving_platform, screen)

        # Обновление и отрисовка пуль
        hero.update_bullets(screen, monsters)

        # Отрисовка монстров
        for monster in monsters:
            monster.draw(screen)

        # Проверка изменения фона
        location.change_background(hero, screen)

        # Пример использования перегруженного оператора +=
        hero += 100  # Увеличиваем счет героя на 100
        print(hero)  # Вывод: "Персонаж: Герой, Счет: 100" (или больше, если счет уже был)

        # Пример использования перегруженного оператора ==
        other_hero = location.Character("Другой герой", location)  # Создаем другого героя
        if hero == other_hero:
            print("Счет героев одинаковый!")
        else:
            print("Счет героев разный!")  # Вывод: "Счет героев разный!"

        # Обновление экрана
        pygame.display.flip()

        # Задержка для демонстрации
        pygame.time.delay(30)