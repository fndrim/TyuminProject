import pygame
import os


pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("High jump")

# Шрифт для текста
font = pygame.font.Font(None, 36)

# Класс Персонаж
class Character:
    def __init__(self, appearance):
        self.appearance = appearance
        self.score = 0

    def shoot(self, target, screen):
        message = f"{self.appearance} стреляет в {target.appearance}!"
        draw_text(screen, message, 50, 100)
        if isinstance(target, Monster):
            target.die(screen)

    def jump(self, platform, screen):
        message = f"{self.appearance} прыгает на {platform.appearance}!"
        draw_text(screen, message, 50, 150)
        platform.interact(self, screen)

# Класс Платформа
class Platform:
    def __init__(self, appearance, platform_type):
        self.appearance = appearance
        self.platform_type = platform_type

    def interact(self, character, screen):
        if self.platform_type == "normal":
            message = f"{character.appearance} отпрыгивает выше!"
            draw_text(screen, message, 50, 200)
            character.score += 100
        elif self.platform_type == "broken":
            message = f"{character.appearance} падает вниз, так как платформа сломалась!"
            draw_text(screen, message, 50, 250)
            character.score -= 50
        elif self.platform_type == "moving":
            message = f"{character.appearance} отпрыгивает от движущейся платформы!"
            draw_text(screen, message, 50, 300)
            character.score += 150

# Класс Локация
class Location:
    def __init__(self):
        self.backgrounds = []  # Список для хранения фонов
        self.current_background_index = 0

    def add_background(self, background_path):
        """Добавляет новый фон в список."""
        if os.path.exists(background_path):
            background = pygame.image.load(background_path).convert()
            self.backgrounds.append(background)
            message = f"Фон {background_path} успешно загружен!"
            draw_text(screen, message, 50, 350)
        else:
            message = f"Ошибка: файл {background_path} не найден."
            draw_text(screen, message, 50, 350)

    def change_background(self, character, screen):
        """Меняет фон в зависимости от счета персонажа."""
        if character.score >= 2000 and len(self.backgrounds) > 2:
            self.current_background_index = 2
        elif character.score >= 1000 and len(self.backgrounds) > 1:
            self.current_background_index = 1
        else:
            self.current_background_index = 0
        message = f"Фон изменен на {self.current_background_index + 1}!"
        draw_text(screen, message, 50, 400)

    def draw_background(self, screen):
        """Отрисовывает текущий фон на экране."""
        if self.backgrounds:
            screen.blit(self.backgrounds[self.current_background_index], (0, 0))

# Класс Монстр
class Monster:
    def __init__(self, appearance):
        self.appearance = appearance

    def die(self, screen):
        message = f"{self.appearance} погибает и исчезает!"
        draw_text(screen, message, 50, 450)

# Функция для отрисовки текста на экране
def draw_text(screen, text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

# взаимодействия классов
if __name__ == "__main__":
    # Создание персонажа
    hero = Character("Герой")

    # Создаем платформы
    normal_platform = Platform("Обычная платформа", "normal")
    broken_platform = Platform("Сломанная платформа", "broken")
    moving_platform = Platform("Движущаяся платформа", "moving")

    # Создание локацию
    location = Location()

    # Загружаем фоны
    location.add_background("background1.png")  # Фон для счета < 1000
    location.add_background("background2.png")  # Фон для счета >= 1000
    location.add_background("background3.png")  # Фон для счета >= 2000

    # Создание монстра
    monster = Monster("монстр")

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Очистка экрана
        screen.fill((0, 0, 0))  # Черный фон

        # Отрисовка текущего фона
        location.draw_background(screen)

        # Пример взаимодействия
        hero.jump(normal_platform, screen)
        hero.jump(broken_platform, screen)
        hero.jump(moving_platform, screen)
        hero.shoot(monster, screen)

        # Проверка изменение фона
        location.change_background(hero, screen)
        hero.score = 1500
        location.change_background(hero, screen)
        hero.score = 2500
        location.change_background(hero, screen)

        # Обновление экрана
        pygame.display.flip()

        # Задержка для демонстрации
        pygame.time.delay(2000)

    # Завершение работы Pygame
    pygame.quit()