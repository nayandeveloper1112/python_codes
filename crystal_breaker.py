import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crystal Breaker")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 40)
BIG = pygame.font.Font(None, 80)

WHITE = (255, 255, 255)
BLACK = (10, 5, 25)
PURPLE = (180, 70, 255)
CYAN = (30, 230, 255)
RED = (255, 60, 80)
ORANGE = (255, 140, 40)
YELLOW = (255, 220, 50)
GREEN = (50, 220, 100)
BLUE = (60, 120, 255)


while True:

    paddle = pygame.Rect(
        WIDTH // 2 - 80,
        HEIGHT - 55,
        160,
        18
    )

    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2

    velocity_x = 400
    velocity_y = -400

    bricks = []

    colors = [
        RED,
        ORANGE,
        YELLOW,
        GREEN,
        BLUE,
        PURPLE
    ]

    for row in range(6):

        for col in range(12):

            bricks.append(
                (
                    pygame.Rect(
                        70 + col * 96,
                        90 + row * 42,
                        84,
                        30
                    ),
                    colors[row]
                )
            )

    score = 0
    lives = 3

    running = True

    while running:

        dt = clock.tick(60) / 1000

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
            paddle.x -= int(700 * dt)

        if keys[pygame.K_RIGHT]:
            paddle.x += int(700 * dt)

        paddle.x = max(
            0,
            min(WIDTH - paddle.width, paddle.x)
        )

        ball_x += velocity_x * dt
        ball_y += velocity_y * dt

        if ball_x < 10 or ball_x > WIDTH - 10:
            velocity_x *= -1

        if ball_y < 70:
            velocity_y *= -1

        ball_rect = pygame.Rect(
            int(ball_x - 9),
            int(ball_y - 9),
            18,
            18
        )

        if (
            ball_rect.colliderect(paddle)
            and velocity_y > 0
        ):
            velocity_y = -abs(velocity_y)

        hit = None

        for brick in bricks:

            if ball_rect.colliderect(brick[0]):

                hit = brick
                break

        if hit:

            bricks.remove(hit)
            score += 10
            velocity_y *= -1

        if ball_y > HEIGHT:

            lives -= 1

            ball_x = WIDTH / 2
            ball_y = HEIGHT / 2

            velocity_x = 400
            velocity_y = -400

            if lives <= 0:
                running = False

        if not bricks:
            running = False

        screen.fill(BLACK)

        screen.blit(
            FONT.render(
                f"Score: {score}    Lives: {lives}",
                True,
                WHITE
            ),
            (20, 20)
        )

        for brick, color in bricks:

            pygame.draw.rect(
                screen,
                color,
                brick,
                border_radius=6
            )

        pygame.draw.rect(
            screen,
            PURPLE,
            paddle,
            border_radius=8
        )

        pygame.draw.circle(
            screen,
            CYAN,
            (int(ball_x), int(ball_y)),
            9
        )

        pygame.display.flip()

    # Result screen
    while True:

        screen.fill(BLACK)

        if not bricks:
            title = "YOU WIN!"
            color = GREEN
        else:
            title = "GAME OVER"
            color = RED

        image = BIG.render(title, True, color)

        screen.blit(
            image,
            image.get_rect(center=(WIDTH // 2, 280))
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
