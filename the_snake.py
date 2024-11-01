from random import randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH,
                                  SCREEN_HEIGHT), 0, 32)


pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс"""

    def __init__(self, body_color=None):
        self.body_color = body_color
        self.surface = screen
        self.board = [[' ' for _ in range(SCREEN_WIDTH)]
                      for _ in range(SCREEN_HEIGHT)]
    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self, surface):
        """Method draw in Base Class"""
        raise NotImplementedError("draw method in GameObject")

    def draw_rect(self, x, y, width, height, color=None):
        """Метод для отрисовки прямоугольника на заданной поверхности."""
        rect = pygame.Rect(x, y, width, height)
        if color is None:
            color = self.body_color
        pygame.draw.rect(self.surface, color, rect)
        pygame.draw.rect(self.surface, BORDER_COLOR, rect, 1)


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
        x, y = self.position
        self.draw_rect(x, y, GRID_SIZE, GRID_SIZE)


class Snake(GameObject):
    """Snake — класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.direction = RIGHT
        self.next_direction = None
        self.positions = self.reset()
        self.length = 1
        self.last = None

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.positions = [self.position]
        screen.fill(BOARD_BACKGROUND_COLOR)
        return self.positions

    def draw(self, surface):
        """Метод draw обрисовывает змейку на поверхности."""
        for i, position in enumerate(self.positions[:-1]):
            x, y = position
            if i == 0 or position != self.last:
                self.draw_rect(x, y, GRID_SIZE, GRID_SIZE, self.body_color)
            else:
                pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR,
                                 (x, y, GRID_SIZE, GRID_SIZE))
        x, y = self.positions[0]
        self.draw_rect(x, y, GRID_SIZE, GRID_SIZE, self.body_color)
        if self.last:
            x, y = self.last
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR,
                             (x, y, GRID_SIZE, GRID_SIZE))

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

        if (obj.get_apple_position() != self.get_head_position()
                and self.get_head_position() in self.positions[2:]):
            self.reset()

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
            # Перерисовываем фоновый цвет на месте предыдущего сегмента
            x, y = self.last
            pygame.draw.rect(self.surface, BOARD_BACKGROUND_COLOR,
                             (x, y, GRID_SIZE, GRID_SIZE))
        else:
            self.last = None

    def get_head_position(self):
        """Метод возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def update_direction(self):
        """Update the direction of the snake."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Метод handle_keys."""
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
    """Метод main."""
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
