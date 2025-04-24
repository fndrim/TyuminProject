import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Израиль jAmp")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Настройки игры
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLATFORM_WIDTH, PLATFORM_HEIGHT = 80, 10  # Размеры платформы
PLAYER_SIZE = 60  # Новый размер игрока


# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Загрузка изображений игрока
        self.image_right = pygame.image.load("image/right_1.png").convert_alpha()
        self.image_left = pygame.image.load("image/left_1.png").convert_alpha()

        # Скалирование изображений до нужного размера (60x60)
        self.image_right = pygame.transform.scale(self.image_right, (PLAYER_SIZE, PLAYER_SIZE))
        self.image_left = pygame.transform.scale(self.image_left, (PLAYER_SIZE, PLAYER_SIZE))

        # Начальное изображение игрока
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = 0
        self.direction = "right"  # Направление движения игрока

    def update(self):
        # Применение гравитации
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Ограничение по нижней границе экрана
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

        # Ограничение по верхней границе экрана
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def move(self, keys):
        # Движение влево/вправо
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.image = self.image_left  # Изменяем изображение на left_1
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.image = self.image_right  # Изменяем изображение на right_1
            self.direction = "right"

        # Ограничение по боковым границам экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


# Базовый класс для платформ
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        # Загрузка изображения платформы
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Класс для синей платформы (движущаяся)
class BluePlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, "image/move_b.png")
        self.speed = 3
        self.direction = 1  # 1 - вправо, -1 - влево

    def update(self):
        self.rect.x += self.speed * self.direction

        # Проверка на достижение границ экрана
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1


# Класс для коричневой платформы (разрушаемая)
class BrownPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, "image/red_b.png")
        self.should_remove = False  # Флаг для удаления платформы


# Функция проверки столкновений игрока с платформами
def check_collision(player, platforms):
    if player.velocity > 0:  # Проверяем только при падении
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            # Проверяем, есть ли среди столкнувшихся платформ не коричневые
            non_brown_hits = [hit for hit in hits if not isinstance(hit, BrownPlatform)]

            if non_brown_hits:
                player.velocity = JUMP_STRENGTH  # Игрок прыгает вверх
            else:
                # Если столкнулись только с коричневыми платформами
                player.velocity = JUMP_STRENGTH
                for hit in hits:
                    if isinstance(hit, BrownPlatform):
                        hit.should_remove = True  # Помечаем платформу на удаление


# Генерация случайных платформ
def generate_platforms():
    platforms = pygame.sprite.Group()

    for i in range(10):
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = i * (HEIGHT // 10)

        # Случайный выбор типа платформы
        platform_type = random.choice(["static", "blue", "brown"])

        if platform_type == "static":
            platform = Platform(x, y, "image/static_b.png")
        elif platform_type == "blue":
            platform = BluePlatform(x, y)
        elif platform_type == "brown":
            platform = BrownPlatform(x, y)

        platforms.add(platform)

    return platforms


# Функция отображения начального экрана
def show_start_screen():
    start_screen_image = pygame.image.load("image/start_screen_bg.png").convert()
    screen.blit(start_screen_image, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Основная функция игры
def main():
    clock = pygame.time.Clock()
    player = Player()
    platforms = generate_platforms()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    running = True
    score = 0

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление игроком (движение влево/вправо)
        keys = pygame.key.get_pressed()
        player.move(keys)  # Обновляем направление движения игрока

        # Обновление игрока и проверка столкновений
        player.update()
        check_collision(player, platforms)

        # Удаление коричневых платформ, помеченных на удаление
        for platform in platforms:
            if isinstance(platform, BrownPlatform) and platform.should_remove:
                platforms.remove(platform)
                all_sprites.remove(platform)

        # Обновление движущихся платформ
        for platform in platforms:
            if isinstance(platform, BluePlatform):
                platform.update()

        # Смещение платформ вниз при подъеме игрока
        if player.rect.top < HEIGHT // 4:
            player.rect.y += abs(player.velocity)
            for platform in platforms:
                platform.rect.y += abs(player.velocity)
                if platform.rect.top > HEIGHT:
                    platform.rect.y = 0
                    platform.rect.x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                    score += 1

        # Отрисовка всех спрайтов
        all_sprites.draw(screen)

        # Отображение счета
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    # Инициализация звука
    pygame.mixer.init()

    # Загрузка и воспроизведение музыки
    pygame.mixer.music.load("image/evrey.mp3")
    pygame.mixer.music.play(-1)  # Воспроизводить в бесконечном цикле

    # Показать начальный экран
    show_start_screen()

    # Запустить основную игру
    main()