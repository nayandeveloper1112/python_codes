import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Dodge")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 40)
BIG = pygame.font.Font(None, 80)

BLACK = (2, 3, 15)
WHITE = (255, 255, 255)
CYAN = (30, 230, 255)
ORANGE = (255, 130, 40)
RED = (220, 50, 40)


while True:

    player_x = WIDTH // 2
    player_y = HEIGHT - 90

    meteors = []

    score = 0
    spawn_timer = 0

    running = True

    while running:

        dt = clock.tick(60) / 1000
        spawn_timer += dt

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
            player_x -= 500 * dt

        if keys[pygame.K_RIGHT]:
            player_x += 500 * dt

        player_x = max(
            25,
            min(WIDTH - 25, player_x)
        )

        if spawn_timer > 0.25:

            spawn_timer = 0

            meteors.append([
                random.randint(20, WIDTH - 20),
                -40,
                random.randint(100, 300),
                random.randint(15, 32)
            ])

        for meteor in meteors[:]:

            x, y, speed, radius = meteor

            meteor[1] += speed * dt

            if meteor[1] > HEIGHT + 50:

                meteors.remove(meteor)
                score += 1
                continue

            distance = math.hypot(
                x - player_x,
                y - player_y
            )

            if distance < radius + 18:

                running = False

        screen.fill(BLACK)

        # Stars
        for i in range(120):

            x = (i * 97) % WIDTH
            y = (i * 53 + score * 3) % HEIGHT

            pygame.draw.circle(
                screen,
                (70, 80, 130),
                (x, y),
                1
            )

        # Spaceship
        pygame.draw.polygon(
            screen,
            CYAN,
            [
                (player_x, player_y - 25),
                (player_x - 22, player_y + 20),
                (player_x + 22, player_y + 20)
            ]
        )

        # Meteors
        for x, y, speed, radius in meteors:

            pygame.draw.circle(
                screen,
                RED,
                (int(x), int(y)),
                radius
            )

            pygame.draw.circle(
                screen,
                ORANGE,
                (
                    int(x - radius * 0.3),
                    int(y - radius * 0.3)
                ),
                max(2, radius // 3)
            )

        screen.blit(
            FONT.render(
                f"METEOR DODGE    Score: {score}",
                True,
                WHITE
            ),
            (20, 20)
        )

        pygame.display.flip()

    # Game over
    while True:

        screen.fill(BLACK)

        image = BIG.render(
            "YOU CRASHED!",
            True,
            RED
        )

        screen.blit(
            image,
            image.get_rect(
                center=(WIDTH // 2, 280)
            )
        )

        screen.blit(
            FONT.render(
                f"Score: {score}",
                True,
                WHITE
            ),
            (WIDTH // 2 - 60, 370)
        )

        screen.blit(
            FONT.render(
                "R = Restart    ESC = Quit",
                True,
                CYAN
            ),
            (WIDTH // 2 - 180, 430)
        )

        pygame.display.flip()

        restart = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    restart = True

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if restart:
            break

        clock.tick(60)
