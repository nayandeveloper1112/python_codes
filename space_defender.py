import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defender")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 40)
BIG = pygame.font.Font(None, 80)

BLACK = (3, 5, 20)
WHITE = (255, 255, 255)
CYAN = (40, 240, 255)
RED = (255, 60, 70)
YELLOW = (255, 220, 50)


def draw_text(message, x, y, color=WHITE):
    screen.blit(FONT.render(str(message), True, color), (x, y))


while True:

    player = pygame.Rect(
        WIDTH // 2 - 30,
        HEIGHT - 80,
        60,
        35
    )

    bullets = []
    enemies = []

    score = 0
    lives = 3

    enemy_timer = 0
    shoot_timer = 0

    running = True

    while running:

        dt = clock.tick(60) / 1000

        enemy_timer += dt
        shoot_timer -= dt

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
            player.x -= int(500 * dt)

        if keys[pygame.K_RIGHT]:
            player.x += int(500 * dt)

        player.x = max(
            0,
            min(WIDTH - player.width, player.x)
        )

        if keys[pygame.K_SPACE] and shoot_timer <= 0:

            bullets.append(
                pygame.Rect(
                    player.centerx - 3,
                    player.top - 20,
                    6,
                    20
                )
            )

            shoot_timer = 0.15

        if enemy_timer > 0.6:

            enemy_timer = 0

            enemies.append(
                pygame.Rect(
                    random.randint(20, WIDTH - 60),
                    -40,
                    40,
                    30
                )
            )

        for bullet in bullets[:]:

            bullet.y -= int(800 * dt)

            if bullet.bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:

            enemy.y += int((150 + score * 0.03) * dt)

            if enemy.top > HEIGHT:

                enemies.remove(enemy)
                lives -= 1

            elif enemy.colliderect(player):

                enemies.remove(enemy)
                lives -= 1

        for bullet in bullets[:]:

            for enemy in enemies[:]:

                if bullet.colliderect(enemy):

                    if bullet in bullets:
                        bullets.remove(bullet)

                    enemies.remove(enemy)

                    score += 10
                    break

        if lives <= 0:
            running = False

        screen.fill(BLACK)

        # Stars
        for i in range(100):
            x = (i * 137) % WIDTH
            y = (i * 71) % HEIGHT

            pygame.draw.circle(
                screen,
                (30, 40, 80),
                (x, y),
                1
            )

        # Spaceship
        pygame.draw.polygon(
            screen,
            CYAN,
            [
                (player.centerx, player.top),
                (player.left, player.bottom),
                (player.right, player.bottom)
            ]
        )

        # Bullets
        for bullet in bullets:
            pygame.draw.rect(
                screen,
                YELLOW,
                bullet
            )

        # Enemies
        for enemy in enemies:

            pygame.draw.rect(
                screen,
                RED,
                enemy,
                border_radius=8
            )

            pygame.draw.circle(
                screen,
                YELLOW,
                enemy.center,
                5
            )

        draw_text(
            f"SPACE DEFENDER   Score: {score}   Lives: {lives}",
            20,
            20
        )

        pygame.display.flip()

    # Game over
    while True:

        screen.fill(BLACK)

        image = BIG.render("GAME OVER", True, RED)
        screen.blit(
            image,
            image.get_rect(center=(WIDTH // 2, 300))
        )

        draw_text(
            f"Final Score: {score}",
            WIDTH // 2 - 100,
            380
        )

        draw_text(
            "R = Restart    ESC = Quit",
            WIDTH // 2 - 180,
            440,
            CYAN
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

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if restart:
            break

        clock.tick(60)
