from random import randint
import pygame

# Constants for screen size and grid
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Speed
SPEED = 20

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects."""

    def __init__(self, position=(0, 0)):
        self.position = position
        self.body_color = None

    def draw(self):
        """Abstract method to draw the object on the screen."""
        pass


class Apple(GameObject):
    """Class representing an apple in the game."""

    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Sets a random position for the apple within the grid."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self):
        """Draws the apple on the screen."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Class representing the snake in the game."""

    def __init__(self):
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Updates the direction of the snake based on user input."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Moves the snake in the current direction."""
        head_x, head_y = self.positions[0]
        move_x, move_y = self.direction
        new_head = ((head_x + move_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + move_y * GRID_SIZE) % SCREEN_HEIGHT)

        if len(self.positions) > 2 and new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def get_head_position(self):
        """Returns the position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to the initial state."""
        self.__init__()

    def draw(self):
        """Draws the snake on the screen."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Handles user input to control the snake."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Main function that runs the game loop."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if name == '__main__':
    main()
