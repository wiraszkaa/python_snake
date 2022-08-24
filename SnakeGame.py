from Game import Game
import pygame


RULES = """Move with arrows
Eat apples to grow and gain score
Don't touch yourself or the walls"""


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
    blit_text(screen, "Weronika Olejarnik", 40, 0, (0, 120))
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
with open('results.txt', 'r') as infile:
    results = infile.read().split("\n")
    if len(results) >= 2:
        for i in range(0, len(results), 2):
            scores.append(Result(int(results[i + 1]), results[i]))
    infile.close()

pygame.init()

bound = (832, 640)
screen = pygame.display.set_mode(bound)

pygame.display.set_caption("Snake")
pygame.display.set_icon(pygame.image.load("snake.png"))

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

with open('results.txt', 'w') as filehandle:
    string = ""
    for result in scores:
        string += result.name
        string += "\n"
        string += str(result.score)
        string += "\n"

    filehandle.write(string[:-1])
    filehandle.close()

pygame.quit()

