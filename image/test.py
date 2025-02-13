import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Настройки персонажа
player_width = 40
player_height = 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 50
player_velocity_y = 0
player_speed = 5

# Настройки платформ
platform_width = 70
platform_height = 20
platforms = []

# Гравитация
gravity = 0.4

# Счетчик высоты
score = 0


# Функция для создания новой платформы
def create_platform():
    platform_x = random.randint(0, WIDTH - platform_width)
    platform_y = platforms[-1][1] - random.randint(50, 150)
    # Убедимся, что платформа не слишком далеко
    if platform_y < 0:
        platform_y = random.randint(50, 150)
    platforms.append([platform_x, platform_y])


# Функция для отрисовки текста
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


# Основной цикл игры
def game_loop():
    global player_x, player_y, player_velocity_y, platforms, score

    # Сброс позиции игрока и счета
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 50
    player_velocity_y = 0
    score = 0

    # Инициализация платформ
    platforms = []
    # Первая платформа всегда под игроком
    platforms.append([player_x - platform_width // 2, HEIGHT - 50])
    # Добавляем еще несколько платформ для начала игры
    for _ in range(5):
        create_platform()

    running = True
    while running:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Движение персонажа
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Гравитация и прыжки
        player_velocity_y += gravity
        player_y += player_velocity_y

        # Проверка столкновений с платформами
        for platform in platforms:
            if (player_y + player_height >= platform[1] and
                    player_y + player_height <= platform[1] + platform_height and
                    player_x + player_width >= platform[0] and
                    player_x <= platform[0] + platform_width and
                    player_velocity_y > 0):
                player_velocity_y = -10  # Прыжок
                # Генерация новой платформы при прыжке
                create_platform()

        # Генерация новых платформ
        while len(platforms) < 6:
            create_platform()

        # Удаление платформ, которые ушли за пределы экрана
        if platforms[0][1] > HEIGHT:
            platforms.pop(0)

        # Отрисовка платформ
        for platform in platforms:
            pygame.draw.rect(screen, BLUE, (platform[0], platform[1], platform_width, platform_height))

        # Отрисовка персонажа
        pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))

        # Обновление счета (высота в пикселях)
        score = max(score, HEIGHT - player_y)

        # Отрисовка счета
        draw_text(f"Счет: {int(score)} м", 30, BLACK, WIDTH - 150, 10)

        # Проверка на проигрыш
        if player_y > HEIGHT:
            running = False

        # Обновление экрана
        pygame.display.update()
        clock.tick(30)

    # Экран проигрыша
    screen.fill(WHITE)
    draw_text("Вы проиграли!", 50, RED, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(f"Ваш счет: {int(score)} м", 40, BLACK, WIDTH // 2, HEIGHT // 2)
    draw_text("Нажмите R, чтобы начать заново", 30, BLACK, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.update()

    # Ожидание нажатия клавиши R для перезапуска
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False


# Запуск игры
clock = pygame.time.Clock()
while True:
    game_loop()