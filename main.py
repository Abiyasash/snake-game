import pygame
from pygame.math import Vector2
from random import randint


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.initial_length = 3

    def draw_snake(self):
        for block in self.body:
            x_pos, y_pos = block.x * CELL_SIZE, block.y * CELL_SIZE
            block_rect = pygame.FRect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            border_thickness = 2
            border_rect = block_rect.inflate(border_thickness, border_thickness)
            pygame.draw.rect(display_surface, SNAKE_BORDER_COLOR, border_rect)

            pygame.draw.rect(display_surface, SNAKE_COLOR, block_rect)

    def move_snake(self):
        body_copy = self.body[:] if self.new_block else self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
        self.new_block = False

    def add_block(self):
        self.new_block = True


class Fruit:
    def __init__(self, snake_body):
        self.randomize(snake_body)

    def draw_fruit(self):
        x_pos, y_pos = self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE
        fruit_rect = pygame.FRect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(display_surface, FRUIT_COLOR, fruit_rect)

    def randomize(self, snake_body):
        while True:
            self.x = randint(0, CELL_NUMBER - 1)
            self.y = randint(0, CELL_NUMBER - 1)
            self.pos = Vector2(self.x, self.y)
            if self.pos not in snake_body:
                break


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit(self.snake.body)
        self.game_active = True
        self.running = True
        self.game_font = pygame.font.Font('PressStart2P-Regular.ttf', 25)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_game_over()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def draw_score(self):
        score = str(len(self.snake.body) - self.snake.initial_length)
        score_surface = self.game_font.render(score, True, SCORE_COLOR)
        score_x = CELL_SIZE * CELL_NUMBER - 60
        score_y = CELL_SIZE * CELL_NUMBER - 40
        score_rect = score_surface.get_frect(center=(score_x, score_y))
        display_surface.blit(score_surface, score_rect)
        bg_rect = pygame.FRect(
            score_rect.left, score_rect.top, score_rect.width, score_rect.height
        )
        pygame.draw.rect(
            display_surface, SCORE_COLOR, bg_rect.inflate(20, 16).move(-1, -3), 5, 10
        )

    def check_collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit.randomize(self.snake.body)
            self.snake.add_block()

    def check_game_over(self):
        if (not 0 <= self.snake.body[0].x < CELL_NUMBER) or (
            not 0 <= self.snake.body[0].y < CELL_NUMBER
        ):
            self.game_active = False
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_active = False

    def game_over(self):
        game_over_surface = self.game_font.render(
            f'GAME OVER\n\nSCORE: {len(self.snake.body) - self.snake.initial_length}\n\nPRESS ANY BUTTON TO RESTART',
            True,
            GAME_OVER_COLOR,
        )
        game_over_rect = game_over_surface.get_frect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        display_surface.blit(game_over_surface, game_over_rect)


pygame.init()
CELL_SIZE = 40
CELL_NUMBER = 20
WINDOW_WIDTH, WINDOW_HEIGHT = CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE
SNAKE_COLOR = '#39FF14'
SNAKE_BORDER_COLOR = '#262626'
FRUIT_COLOR = '#FF3131'
BG_COLOR = '#000000'
SCORE_COLOR = '#F1FF70'
GAME_OVER_COLOR = '#FF3CAC'
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

game = Game()

display_update = pygame.event.custom_type()
pygame.time.set_timer(display_update, 150)

while game.running:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        if game.game_active and event.type == display_update:
            game.update()
        if game.game_active and event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP or event.key == pygame.K_w
            ) and game.snake.direction.y != 1:
                game.snake.direction = Vector2(0, -1)
            elif (
                event.key == pygame.K_DOWN or event.key == pygame.K_s
            ) and game.snake.direction.y != -1:
                game.snake.direction = Vector2(0, 1)
            elif (
                event.key == pygame.K_LEFT or event.key == pygame.K_a
            ) and game.snake.direction.x != 1:
                game.snake.direction = Vector2(-1, 0)
            elif (
                event.key == pygame.K_RIGHT or event.key == pygame.K_d
            ) and game.snake.direction.x != -1:
                game.snake.direction = Vector2(1, 0)
        if not game.game_active and event.type == pygame.KEYDOWN:
            game = Game()

    if game.game_active:
        display_surface.fill(BG_COLOR)
        game.draw_elements()
    else:
        game.game_over()
    pygame.display.update()

pygame.quit()
