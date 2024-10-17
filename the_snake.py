from random import choice, randint

import pygame

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self, body_color=None,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Это абстрактный метод, который предназначен
        для переопределения в дочерних классах. Этот
        метод должен определять, как объект будет
        отрисовываться на экране. По умолчанию — pass.
        """
        raise NotImplementedError(
            f'Определите draw в {self.__class__.__name__}.'
        )

    def draw_cell(self, position):
        """Отрисовка ячейки"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко
    и действия с ним. Яблоко должно отображаться в случайных
    клетках игрового поля.
    """

    def __init__(self, positions=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]):
        super().__init__(APPLE_COLOR)
        self.randomize_position(positions)

    def randomize_position(self, positions):
        """Устанавливает случайное положение яблока на игровом поле — задаёт
        атрибуту position новое значение. Координаты выбираются так, чтобы
        яблоко оказалось в пределах игрового поля.
        """
        while self.position in positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку
    и её поведение. Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.reset()

    def update_direction(self, next_direction):
        """Обновляет направление движения змейки"""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        x_position, y_position = self.direction
        head_x = (head_x + x_position * GRID_SIZE) % SCREEN_WIDTH
        head_y = (head_y + y_position * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (head_x, head_y))

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.next_direction = None
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice((UP, DOWN, RIGHT, LEFT))
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы
    изменить направление движения змейки.
    """
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
    """Основной цикл программы"""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        pygame.display.update()


if __name__ == '__main__':
    main()
