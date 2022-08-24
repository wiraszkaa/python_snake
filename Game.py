import math
import pygame
from random import randint
from Snake import Snake, Direction


class Game:

    def __init__(self, screen, bounds):
        self.screen = screen
        self.bound = bounds
        self.score = 0

    def start(self) -> tuple:
        snake = Snake(self.bound)

        pygame.mixer.music.load("background.mp3")
        pygame.mixer.music.play(-1)

        running = True
        apple = None
        while running:
            if apple is None:
                apple = (randint(1, 12) * 64, randint(1, 9) * 64)

            apple = apple_collision(snake, apple)
            if apple is None:
                self.score += 1

            if 32 <= snake.head.pos[0] <= self.bound[0] - 32 and 32 <= snake.head.pos[1] <= self.bound[1] - 32:
                snake.move(1)
                pygame.time.delay(8)
            else:
                game_over(self.screen)
                break

            if body_collision(self.screen, snake):
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(Direction.RIGHT)

            self.screen.fill((0, 150, 0))
            draw_apple(self.screen, apple)
            draw_snake(self.screen, snake)
            self.screen.blit(pygame.font.SysFont('comicsans', 20, True).render(f"Score: {self.score}", True, (255, 255, 255)), (0, 0))
            pygame.display.update()

        return running, self.score


def rotation(direction: Direction):
    match direction:
        case Direction.UP:
            return 180
        case Direction.DOWN:
            return 0
        case Direction.LEFT:
            return 270
        case _:
            return 90


def draw_snake(screen, snake):
    head_img = pygame.image.load("head.png")
    body_img = pygame.image.load("body.png")
    tail_img = pygame.image.load("tail.png")
    pos = snake.head.pos - 32
    screen.blit(pygame.transform.rotate(head_img, rotation(snake.direction)), (pos[0], pos[1]))
    for i, segment in enumerate(snake.body):
        body_pos = segment.pos - 32
        direction = snake.moves[segment.command].direction
        if i == len(snake.body) - 1:
            screen.blit(pygame.transform.rotate(tail_img, rotation(direction)), (body_pos[0], body_pos[1]))
        else:
            screen.blit(pygame.transform.rotate(body_img, rotation(direction)), (body_pos[0], body_pos[1]))


def draw_apple(screen, apple):
    apple_img = pygame.image.load("apple.png")
    if apple is not None:
        screen.blit(apple_img, (apple[0] - 32, apple[1] - 32))


def apple_collision(snake, apple: tuple):
    distance = math.pow(apple[0] - snake.head.pos[0], 2) + math.pow(apple[1] - snake.head.pos[1], 2)
    if distance <= 700:
        pygame.mixer.Sound("eat.wav").play()
        snake.add_segment()
        return None
    else:
        return apple


def body_collision(screen, snake) -> bool:
    for segment in snake.body:
        distance = math.pow(segment.pos[0] - snake.head.pos[0], 2) + math.pow(segment.pos[1] - snake.head.pos[1], 2)
        if distance < 1000:
            game_over(screen)
            return True
    return False


def game_over(screen):
    pygame.mixer.music.stop()
    pygame.mixer.Sound("game_over.wav").play()
    text = pygame.font.SysFont('comicsans', 120, True).render('Game Over', True, (255, 255, 255))
    screen.blit(text, (100, 180))
    pygame.display.update()
    pygame.time.delay(2500)

