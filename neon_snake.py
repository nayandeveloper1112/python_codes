import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
CELL = 24

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 42)
BIG = pygame.font.Font(None, 80)

BLACK = (5, 8, 20)
CYAN = (0, 240, 255)
BLUE = (30, 100, 255)
RED = (255, 50, 80)
WHITE = (255, 255, 255)


def text(message, x, y, color=WHITE, font=FONT):
    image = font.render(str(message), True, color)
    screen.blit(image, (x, y))


def game_over(score):
    while True:
        screen.fill(BLACK)

        image = BIG.render("GAME OVER", True, RED)
        screen.blit(image, image.get_rect(center=(WIDTH // 2, 280)))

        text(f"Score: {score}", WIDTH // 2 - 70, 370)
        text("R = Restart     ESC = Quit",
             WIDTH // 2 - 180, 430, CYAN)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

        clock.tick(60)


while True:

    cols = WIDTH // CELL
    rows = (HEIGHT - 70) // CELL

    snake = [(cols // 2, rows // 2)]
    direction = (1, 0)

    food = (
        random.randrange(cols),
        random.randrange(rows)
    )

    score = 0
    timer = 0
    speed = 9
    alive = True

    while alive:

        dt = clock.tick(60) / 1000
        timer += dt

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)

                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)

                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)

                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        if timer >= 1 / speed:

            timer = 0

            head = (
                snake[0][0] + direction[0],
                snake[0][1] + direction[1]
            )

            if (
                head[0] < 0
                or head[0] >= cols
                or head[1] < 0
                or head[1] >= rows
                or head in snake
            ):
                alive = False
                continue

            snake.insert(0, head)

            if head == food:

                score += 10
                speed = min(20, 9 + score // 50)

                while food in snake:
                    food = (
                        random.randrange(cols),
                        random.randrange(rows)
                    )

            else:
                snake.pop()

        screen.fill(BLACK)

        text(f"NEON SNAKE     Score: {score}", 20, 20, CYAN)

        for i, (x, y) in enumerate(snake):

            color = CYAN if i == 0 else BLUE

            pygame.draw.rect(
                screen,
                color,
                (
                    x * CELL,
                    y * CELL + 70,
                    CELL - 2,
                    CELL - 2
                ),
                border_radius=6
            )

        pygame.draw.circle(
            screen,
            RED,
            (
                food[0] * CELL + CELL // 2,
                food[1] * CELL + 70 + CELL // 2
            ),
            CELL // 2 - 3
        )

        pygame.display.flip()

    if not game_over(score):
        break

pygame.quit()
