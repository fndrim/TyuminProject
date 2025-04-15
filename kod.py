import pygame
import random
import logging  # модуль логирования

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщений
    filename='game.log',  # Файл для записи логов
    filemode='w'  # Режим записи ('w' - перезапись, 'a' - добавление)
)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump")

# Шрифт для текста
font = pygame.font.Font(None, 36)

# Класс для кнопок
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        """Отрисовка кнопки."""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """Проверка, была ли кнопка нажата."""
        return (self.x <= pos[0] <= self.x + self.width and
                self.y <= pos[1] <= self.y + self.height)

    def check_hover(self, pos):
        """Проверка, находится ли курсор над кнопкой."""
        self.is_hovered = (self.x <= pos[0] <= self.x + self.width and
                           self.y <= pos[1] <= self.y + self.height)

# Класс для главного меню
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.start_button = Button("Начать игру", SCREEN_WIDTH // 2 - 100, 200, 200, 50, BLUE, RED)
        self.exit_button = Button("Выход", SCREEN_WIDTH // 2 - 100, 300, 200, 50, BLUE, RED)

    def display_menu(self):
        """Отображает главное меню и обрабатывает события."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_clicked(event.pos):
                        logging.info("Кнопка 'Начать игру' нажата.")
                        print("Игровой процесс начинается...")
                        return "start_game"
                    elif self.exit_button.is_clicked(event.pos):
                        logging.info("Кнопка 'Выход' нажата.")
                        print("Выход из игры.")
                        pygame.quit()
                        quit()

            # Проверка наведения курсора
            mouse_pos = pygame.mouse.get_pos()
            self.start_button.check_hover(mouse_pos)
            self.exit_button.check_hover(mouse_pos)

            # Отрисовка меню
            self.screen.fill(WHITE)
            self.start_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            pygame.display.flip()

# Класс Character
class Character:
    def __init__(self, appearance, location):
        self.appearance = appearance
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 150
        self.velocity = 0
        self.location = location

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 30, 30))

    def update(self):
        self.velocity += 0.5  # Гравитация
        self.y += self.velocity

        # Ограничение скорости падения
        if self.velocity > 10:
            self.velocity = 10

        # Проверка на выход за границы экрана
        if self.x < 0 or self.x > SCREEN_WIDTH:
            logging.warning("Персонаж вышел за границы экрана по горизонтали")
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            logging.warning("Персонаж вышел за границы экрана по вертикали")

    def check_collision(self):
        for platform in self.location.platforms[:]:
            if (self.y + 30 >= platform.y and
                self.y + 30 <= platform.y + 10 and
                self.x + 30 > platform.x and
                self.x < platform.x + 80):
                platform.interact(self, screen)

# Класс Location
class Location:
    def __init__(self):
        self.platforms = []
        self.generate_initial_platforms()

    def generate_initial_platforms(self):
        platform_count = 10
        try:
            for i in range(platform_count):
                x = random.randint(0, SCREEN_WIDTH - 80)
                y = i * (SCREEN_HEIGHT // platform_count)
                platform_type = "normal" if random.random() > 0.2 else "broken"
                self.platforms.append(self.Platform("Платформа", platform_type, x, y))

            # Добавление начальной платформы под персонажем
            start_platform = self.Platform("Стартовая платформа", "normal", SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 150)
            self.platforms.append(start_platform)
        except Exception as e:
            logging.error(f"Ошибка при генерации платформ: {e}")
        finally:
            logging.info("Генерация платформ завершена.")

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

            # Проверка на наличие платформ
            if not self.platforms:
                logging.warning("Список платформ пуст")
        except Exception as e:
            logging.error(f"Ошибка при обновлении платформ: {e}")
        finally:
            logging.info("Обновление платформ завершено.")

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

# Функция для отрисовки текста
def draw_text(screen, text, x, y):
    """
    Отрисовывает текст на экране.
    :param screen: Экран pygame.
    :param text: Текст для отображения.
    :param x: Координата X.
    :param y: Координата Y.
    """
    text_surface = font.render(text, True, WHITE)  # Белый цвет текста
    screen.blit(text_surface, (x, y))

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
    logging.info("Сброс игры завершен.")

# Основной код игры
if __name__ == "__main__":
    menu = Menu(screen)
    action = menu.display_menu()  # Показываем главное меню

    if action == "start_game":
        location = Location()
        hero = Character("Герой", location)

        running = True
        game_over = False  # Флаг для состояния "Game Over"
        clock = pygame.time.Clock()

        while running:
            screen.fill(WHITE)  # Белый фон
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
                    logging.info("Игрок упал за пределы экрана!")
                    game_over = True  # Переход в состояние "Game Over"
            else:
                # Экран "Game Over"
                draw_text(screen, "Игра окончена", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
                draw_text(screen, "Нажмите ПРОБЕЛ для перезапуска", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)

            # Отрисовка
            location.draw_platforms(screen)
            hero.draw(screen)
            draw_text(screen, f"Y: {int(hero.y)}", 10, 10)

            # Обновление экрана
            pygame.display.flip()

        pygame.quit()