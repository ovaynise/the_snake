from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH,
                                  SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс"""

    def __init__(self, body_color=None):
        self.body_color = body_color
        self.board = [[' ' for _ in range(SCREEN_WIDTH)]
                      for _ in range(SCREEN_HEIGHT)]
    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self, surface):
        """ Method draw in Base Class"""
        raise NotImplementedError("draw method in GameObject")


class Apple(GameObject):
    """Класс обрисовывающий яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position(GRID_SIZE)

    @staticmethod
    def randomize_position(grid_size):
        """Метод возвращает случайную позицию яблока."""
        return (randint(0, GRID_WIDTH - 1)
                * grid_size, randint(0, GRID_HEIGHT - 1) * grid_size)

    def get_apple_position(self):
        """Метод возвращающий позицию яблока."""
        return self.position

    def update_apple_position(self):
        """Метод обновляет позицию яблока."""
        self.position = self.randomize_position(GRID_SIZE)
        return self.position

    def draw(self, surface):
        """Метод обрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
             (self.position[0], self.position[1]),
             (GRID_SIZE, GRID_SIZE)
            )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake — класс, унаследованный от GameObject,
     описывающий змейку и её поведение. Этот класс управляет
     её движением, рисует, а также обрабатывает действия пользователя.
     """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.length = 1
        self.last = None

    def draw(self, surface):
        """Метод draw обрисовывает змейку на поверхности."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        print(self.positions[1])

        self.positions = [self.position]
        screen.fill(BOARD_BACKGROUND_COLOR)

    def move(self, obj):
        """Метод move. Отвечает за движение змейки и события."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, position)
        if obj.get_apple_position() == self.get_head_position():
            self.positions.insert(0, position)
            obj.update_apple_position()
            print(f'Длинна змейки составляет:{len(self.positions)-1}')

        if (obj.get_apple_position() != self.get_head_position()
                and self.get_head_position() in self.positions[2:]):
            print('Мы попали в змейку')
            self.reset()

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Update the direction of the snake."""

        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """ Метод handle_keys."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """ Метод main."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
