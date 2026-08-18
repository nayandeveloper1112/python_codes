import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Highway Racer")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 40)
BIG = pygame.font.Font(None, 80)

WHITE = (255, 255, 255)
GREEN = (30, 120, 50)
ROAD = (45, 45, 50)
YELLOW = (255, 220, 50)
CYAN = (30, 220, 255)
RED = (255, 60, 70)


def text(msg, x, y, color=WHITE):
    screen.blit(FONT.render(str(msg), True, color), (x, y))


while True:

    car = pygame.Rect(
        WIDTH // 2 - 25,
        HEIGHT - 120,
        50,
        80
    )

    enemies = []

    lanes = [
        400,
        615,
        830
    ]

    score = 0
    speed = 350
    timer = 0

    running = True

    while running:

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

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            car.x -= int(500 * dt)

        if keys[pygame.K_RIGHT]:
            car.x += int(500 * dt)

        car.x = max(300, min(930, car.x))

        if timer > 0.7:

            timer = 0

            enemies.append(
                pygame.Rect(
                    random.choice(lanes),
                    -100,
                    55,
                    85
                )
            )

        for enemy in enemies[:]:

            enemy.y += int(speed * dt)

            if enemy.top > HEIGHT:

                enemies.remove(enemy)

                score += 10
                speed = min(700, speed + 5)

            elif enemy.colliderect(car):

                running = False

        screen.fill(GREEN)

        # Road
        pygame.draw.rect(
            screen,
            ROAD,
            (280, 0, 720, HEIGHT)
        )

        # Road borders
        pygame.draw.line(
            screen,
            YELLOW,
            (285, 0),
            (285, HEIGHT),
            6
        )

        pygame.draw.line(
            screen,
            YELLOW,
            (995, 0),
            (995, HEIGHT),
            6
        )

        # Lane lines
        for x in [500, 715, 930]:

            for y in range(0, HEIGHT, 80):

                pygame.draw.rect(
                    screen,
                    WHITE,
                    (x, y, 8, 40)
                )

        # Player car
        pygame.draw.rect(
            screen,
            CYAN,
            car,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (
                car.x + 8,
                car.y + 12,
                34,
                25
            ),
            border_radius=5
        )

        # Enemy cars
        for enemy in enemies:

            pygame.draw.rect(
                screen,
                RED,
                enemy,
                border_radius=12
            )

        text(
            f"HIGHWAY RACER    Score: {score}",
            20,
            20
        )

        pygame.display.flip()

    # Game over
    while True:

        screen.fill((10, 10, 20))

        image = BIG.render("CRASH!", True, RED)

        screen.blit(
            image,
            image.get_rect(center=(WIDTH // 2, 280))
        )

        text(
            f"Score: {score}",
            WIDTH // 2 - 60,
            370
        )

        text(
            "R = Restart    ESC = Quit",
            WIDTH // 2 - 180,
            430,
            CYAN
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    break

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        else:
            clock.tick(60)
            continue

        break
