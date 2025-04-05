import pygame
import random

# Создание пользовательского исключения
class CustomError(Exception):
    """Основное пользовательское исключение."""
    pass

class SpecificError(CustomError):
    """Дочернее пользовательское исключение."""
    pass

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump")

# Шрифт для текста
font = pygame.font.Font(None, 36)

# Функция для отрисовки текста
def draw_text(screen, text, x, y):
    """
    Отрисовывает текст на экране.
    :param screen: Экран pygame.
    :param text: Текст для отображения.
    :param x: Координата X.
    :param y: Координата Y.
    """
    text_surface = font.render(text, True, (255, 255, 255))  # Белый цвет текста
    screen.blit(text_surface, (x, y))

# Базовый класс с защищенными атрибутами
class BaseClass:
    def __init__(self, name):
        self._name = name  # Защищенный атрибут
        self._protected_value = 42  # Защищенный атрибут

    def base_method(self):
        print(f"Это метод базового класса {self._name}")

    def common_method(self):
        print(f"Это общий метод из базового класса {self._name}. Защищенное значение: {self._protected_value}")

    def __str__(self):
        return f"Объект класса BaseClass: имя={self._name}, защищенное значение={self._protected_value}"

    def __repr__(self):
        return f"BaseClass(name='{self._name}')"

# Производный класс
class DerivedClass(BaseClass):
    def __init__(self, name):
        super().__init__(name)  # Вызов конструктора базового класса

    def base_method(self):  # Переопределение метода базового класса
        print(f"Это переопределенный метод из производного класса {self._name}")

    def use_protected_attributes(self):
        print(f"Доступ к защищенному атрибуту _name: {self._name}")
        print(f"Доступ к защищенному атрибуту _protected_value: {self._protected_value}")

    def __str__(self):
        return f"Объект класса DerivedClass: имя={self._name}, защищенное значение={self._protected_value}"

    def __repr__(self):
        return f"DerivedClass(name='{self._name}')"

# Класс Location
class Location:
    def __init__(self):
        self.platforms = []
        self.generate_initial_platforms()

    def generate_initial_platforms(self):
        platform_count = 10
        for i in range(platform_count):
            x = random.randint(0, SCREEN_WIDTH - 80)
            y = i * (SCREEN_HEIGHT // platform_count)
            platform_type = "normal" if random.random() > 0.2 else "broken"
            self.platforms.append(self.Platform("Платформа", platform_type, x, y))

        # Добавление начальной платформы под персонажем
        start_platform = self.Platform("Стартовая платформа", "normal", SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 150)
        self.platforms.append(start_platform)

    def draw_platforms(self, screen):
        for platform in self.platforms:
            platform.draw(screen)

    def update_platforms(self, character):
        try:
            for platform in self.platforms[:]:
                if platform.is_off_screen():
                    self.platforms.remove(platform)
                    new_x = random.randint(0, SCREEN_WIDTH - 80)
                    new_y = 0
                    new_type = "normal" if random.random() > 0.2 else "broken"
                    self.platforms.append(self.Platform("Платформа", new_type, new_x, new_y))

            # Проверка, что всегда есть платформа для прыжка
            if all(platform.y > character.y + SCREEN_HEIGHT // 3 for platform in self.platforms):
                new_x = random.randint(0, SCREEN_WIDTH - 80)
                new_y = character.y - 100
                new_type = "normal"
                self.platforms.append(self.Platform("Платформа", new_type, new_x, new_y))
        except Exception as e:
            print(f"Произошла ошибка при обновлении платформ: {e}")
            raise SpecificError("Ошибка при обновлении платформ") from e
        finally:
            print("Обновление платформ завершено.")

    class Platform:
        def __init__(self, appearance, platform_type, x, y):
            self.appearance = appearance
            self.platform_type = platform_type
            self.x = x
            self.y = y

        def draw(self, screen):
            color = (0, 0, 0) if self.platform_type == "normal" else (255, 0, 0)
            pygame.draw.rect(screen, color, (self.x, self.y, 80, 10))

        def interact(self, character, screen):
            if self.platform_type == "normal":
                character.velocity = -10  # Прыжок
            elif self.platform_type == "broken":
                self.x = -100  # Убираем платформу с экрана
                # Генерация новой платформы
                new_x = random.randint(0, SCREEN_WIDTH - 80)
                new_y = self.y - 100
                new_type = "normal"
                character.location.platforms.append(character.location.Platform("Платформа", new_type, new_x, new_y))

        def is_off_screen(self):
            return self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT

# Класс Character
class Character:
    def __init__(self, appearance, location):
        self.appearance = appearance
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 150
        self.velocity = 0
        self.location = location

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, 30, 30))

    def update(self):
        try:
            self.velocity += 0.5  # Гравитация
            self.y += self.velocity

            # Ограничение скорости падения
            if self.velocity > 10:
                self.velocity = 10
        except Exception as e:
            print(f"Произошла ошибка при обновлении персонажа: {e}")
            raise SpecificError("Ошибка при обновлении персонажа") from e
        finally:
            print("Обновление персонажа завершено.")

    def check_collision(self):
        for platform in self.location.platforms[:]:
            if (self.y + 30 >= platform.y and
                self.y + 30 <= platform.y + 10 and
                self.x + 30 > platform.x and
                self.x < platform.x + 80):
                platform.interact(self, screen)

# Функция для сброса игры
def reset_game(location, hero):
    """
    Сбрасывает состояние игры.
    :param location: Объект класса Location.
    :param hero: Объект класса Character.
    """
    hero.x = SCREEN_WIDTH // 2
    hero.y = SCREEN_HEIGHT - 150
    hero.velocity = 0
    location.platforms.clear()
    location.generate_initial_platforms()

# Основной код игры
if __name__ == "__main__":
    location = Location()
    hero = Character("Герой", location)

    running = True
    game_over = False  # Флаг для состояния "Game Over"
    clock = pygame.time.Clock()

    while running:
        screen.fill((255, 255, 255))  # Белый фон
        clock.tick(60)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Перезапуск игры при нажатии на пробел
                reset_game(location, hero)
                game_over = False

        if not game_over:
            # Управление персонажем
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                hero.x -= 5
            if keys[pygame.K_RIGHT]:
                hero.x += 5

            # Обновление состояния
            hero.update()
            hero.check_collision()
            location.update_platforms(hero)

            # Проверка на падение игрока
            if hero.y > SCREEN_HEIGHT:
                print("Игрок упал за пределы экрана!")  # Отладочное сообщение
                game_over = True  # Переход в состояние "Game Over"
        else:
            # Экран "Game Over"
            draw_text(screen, "Игра окончена", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
            draw_text(screen, "Нажмите ПРОБЕЛ для перезапуска", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)

        # Отрисовка
        location.draw_platforms(screen)
        hero.draw(screen)

        # Отображение координат игрока (для отладки)
        draw_text(screen, f"Y: {int(hero.y)}", 10, 10)

        # Обновление экрана
        pygame.display.flip()

    pygame.quit()