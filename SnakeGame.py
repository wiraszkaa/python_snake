import pygame
from enum import Enum
import numpy as np
import math
from random import randint


RULES = """Move with arrows
Eat apples to grow and gain score
Don't touch yourself or the walls"""


class Direction(Enum):
    UP = -1
    DOWN = 1
    LEFT = -2
    RIGHT = 2


class Segment:
    def __init__(self, pos, command: int):
        self.pos = pos
        self.command = command


class Move:
    def __init__(self, direction: Direction, pos):
        self.pos = pos
        self.direction = direction


class Snake:
    def __init__(self, bounds: tuple):
        self.bounds = bounds
        self.body = []
        self.head = None
        self.direction = None
        self.moves = []
        self.respawn()

    def respawn(self):
        self.body = []
        self.head = Segment(np.array([32.0, 32.0], dtype=float), 0)
        self.direction = Direction.RIGHT
        self.moves = [Move(self.direction, np.copy(self.head.pos))]

    def change_direction(self, direction: Direction):
        change = False
        match direction:
            case Direction.UP:
                if self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                    change = True
            case Direction.DOWN:
                if self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                    change = True
            case Direction.LEFT:
                if self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                    change = True
            case _:
                if self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                    change = True
        if change:
            self.moves.append(Move(self.direction, self.head.pos))
            self.head.command += 1

    def move(self, distance: float):
        self.head.pos = change_pos(self.head.pos, self.direction, distance)
        for segment in self.body:
            self.move_segment(segment, distance)

    def move_segment(self, segment: Segment, distance: float):
        command = self.moves[segment.command]

        finish_pos = None
        if segment.command + 1 < len(self.moves):
            finish_pos = self.moves[segment.command + 1].pos
        segment.pos = change_pos(segment.pos, command.direction, distance)
        if (segment.pos == finish_pos).all():
            segment.command += 1

    def add_segment(self):
        last = self.head
        if len(self.body) > 0:
            last = self.body[-1]
        self.body.append(Segment(change_pos(last.pos, self.moves[last.command].direction, -64), last.command))


def change_pos(pos, direction: Direction, distance: float):
    pos = np.copy(pos)
    match direction:
        case Direction.UP:
            pos[1] -= distance
            pos[1] = round(pos[1], 2)
            return pos
        case Direction.DOWN:
            pos[1] += distance
            pos[1] = round(pos[1], 2)
            return pos
        case Direction.LEFT:
            pos[0] -= distance
            pos[0] = round(pos[0], 2)
            return pos
        case _:
            pos[0] += distance
            pos[0] = round(pos[0], 2)
            return pos


class Game:

    def __init__(self, screen, bounds):
        self.screen = screen
        self.bound = bounds
        self.score = 0

    def start(self) -> tuple:
        snake = Snake(self.bound)

        pygame.mixer.music.load("data/background.mp3")
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
    head_img = pygame.image.load("data/head.png")
    body_img = pygame.image.load("data/body.png")
    tail_img = pygame.image.load("data/tail.png")
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
    apple_img = pygame.image.load("data/apple.png")
    if apple is not None:
        screen.blit(apple_img, (apple[0] - 32, apple[1] - 32))


def apple_collision(snake, apple: tuple):
    distance = math.pow(apple[0] - snake.head.pos[0], 2) + math.pow(apple[1] - snake.head.pos[1], 2)
    if distance <= 700:
        pygame.mixer.Sound("data/eat.wav").play()
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
    pygame.mixer.Sound("data/game_over.wav").play()
    text = pygame.font.SysFont('comicsans', 120, True).render('Game Over', True, (255, 255, 255))
    screen.blit(text, (100, 180))
    pygame.display.update()
    pygame.time.delay(2500)


class Result:
    def __init__(self, score, name):
        self.score = score
        self.name = name


def blit_text(screen, text: str, fontSize: int, space: int, xy: tuple):
    text = text.split("\n")
    for i in range(len(text)):
        line = pygame.font.SysFont('comicsans', fontSize, True).render(text[i], True, (255, 255, 255))
        screen.blit(line, (xy[0], xy[1] + (fontSize * i) + space))


def rules(screen) -> bool:
    screen.fill((0, 150, 0))
    blit_text(screen, "RULES", 100, 0, (0, 0))
    blit_text(screen, RULES, 40, 0, (0, 120))
    pygame.display.update()
    running = True
    back = False
    while running and not back:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    back = True

    return running


def author(screen) -> bool:
    screen.fill((0, 150, 0))
    blit_text(screen, "AUTHOR", 100, 0, (0, 0))
    blit_text(screen, "Jakub Wiraszka", 40, 0, (0, 120))
    pygame.display.update()
    running = True
    back = False
    while running and not back:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    back = True

    return running


def best(screen) -> bool:
    screen.fill((0, 150, 0))
    blit_text(screen, "BEST SCORES", 100, 0, (0, 0))
    scores.sort(key=lambda x: x.score, reverse=True)
    for i, score in enumerate(scores):
        blit_text(screen, f"{i + 1}. {score.name} Score: {score.score}", 40, 0, (0, 110 + i * 50))
        if i == 9:
            break

    pygame.display.update()
    running = True
    back = False
    while running and not back:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    back = True

    return running


def name(screen) -> tuple:
    name = ""

    running = True
    back = False
    while running and not back:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    back = True
                    break
                else:
                    name += event.unicode
        screen.fill((0, 150, 0))
        blit_text(screen, "WRITE YOUR NAME", 70, 0, (0, 0))
        blit_text(screen, name, 40, 0, (0, 120))
        pygame.display.update()

    return running, name


scores = []
with open('data/results.txt', 'r') as infile:
    results = infile.read().split("\n")
    if len(results) >= 2:
        for i in range(0, len(results), 2):
            scores.append(Result(int(results[i + 1]), results[i]))
    infile.close()

pygame.init()

bound = (832, 640)
screen = pygame.display.set_mode(bound)

pygame.display.set_caption("Snake")
pygame.display.set_icon(pygame.image.load("data/snake.png"))

running = True
pointer = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pointer -= 1
                if pointer == -1:
                    pointer = 3
            elif event.key == pygame.K_DOWN:
                pointer += 1
                if pointer == 4:
                    pointer = 0
            elif event.key == pygame.K_RETURN:
                match pointer:
                    case 0:
                        running, score = Game(screen, bound).start()
                        if not running:
                            break
                        running, name = name(screen)
                        scores.append(Result(score, name))
                        break
                    case 1:
                        running = rules(screen)
                        break
                    case 2:
                        running = best(screen)
                        break
                    case 3:
                        running = author(screen)
                        break
    screen.fill((0, 150, 0))
    blit_text(screen, "PLAY\nRULES\nBEST SCORES\nCREDITS", 100, 0, (100, 0))
    r_start = (45, 50 + 100 * pointer)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(r_start, (50, 50)))
    pygame.display.update()

with open('data/results.txt', 'w') as filehandle:
    string = ""
    for result in scores:
        string += result.name
        string += "\n"
        string += str(result.score)
        string += "\n"

    filehandle.write(string[:-1])
    filehandle.close()

pygame.quit()

