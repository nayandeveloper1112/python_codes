import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arena Shooter")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 38)
BIG = pygame.font.Font(None, 80)

BLACK = (8, 8, 15)
WHITE = (255, 255, 255)
RED = (255, 50, 60)
GREEN = (50, 230, 100)
CYAN = (40, 220, 255)
YELLOW = (255, 220, 40)

player = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
bullets = []
enemies = []

score = 0
health = 100
spawn_timer = 0
shoot_timer = 0

running = True

while running:

    dt = clock.tick(60) / 1000
    spawn_timer += dt
    shoot_timer -= dt

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and shoot_timer <= 0:

                mouse = pygame.Vector2(pygame.mouse.get_pos())
                direction = mouse - player

                if direction.length() > 0:
                    direction.normalize()

                    bullets.append([
                        player.copy(),
                        direction * 900
                    ])

                    shoot_timer = 0.12

    keys = pygame.key.get_pressed()

    movement = pygame.Vector2(
        keys[pygame.K_d] - keys[pygame.K_a],
        keys[pygame.K_s] - keys[pygame.K_w]
    )

    if movement.length():
        movement.normalize()
        player += movement * 420 * dt

    player.x = max(25, min(WIDTH - 25, player.x))
    player.y = max(25, min(HEIGHT - 25, player.y))

    # Spawn enemies
    if spawn_timer > 0.7:

        spawn_timer = 0

        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            pos = pygame.Vector2(random.randint(0, WIDTH), -30)

        elif side == "bottom":
            pos = pygame.Vector2(random.randint(0, WIDTH), HEIGHT + 30)

        elif side == "left":
            pos = pygame.Vector2(-30, random.randint(0, HEIGHT))

        else:
            pos = pygame.Vector2(WIDTH + 30, random.randint(0, HEIGHT))

        enemies.append(pos)

    # Bullets
    for bullet in bullets[:]:

        bullet[0] += bullet[1] * dt

        if not screen.get_rect().inflate(100, 100).collidepoint(bullet[0]):
            bullets.remove(bullet)

    # Enemies
    for enemy in enemies[:]:

        direction = player - enemy

        if direction.length():
            direction.normalize()
            enemy += direction * 150 * dt

        if enemy.distance_to(player) < 35:

            health -= 30 * dt

        # Bullet collision
        for bullet in bullets[:]:

            if enemy.distance_to(bullet[0]) < 25:

                enemies.remove(enemy)

                if bullet in bullets:
                    bullets.remove(bullet)

                score += 10
                break

    if health <= 0:
        running = False

    # Draw
    screen.fill(BLACK)

    # Arena grid
    for x in range(0, WIDTH, 50):
        pygame.draw.line(screen, (18, 18, 30), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (18, 18, 30), (0, y), (WIDTH, y))

    # Player
    pygame.draw.circle(
        screen,
        CYAN,
        (int(player.x), int(player.y)),
        25
    )

    # Bullets
    for bullet in bullets:
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(bullet[0].x), int(bullet[0].y)),
            6
        )

    # Enemies
    for enemy in enemies:
        pygame.draw.circle(
            screen,
            RED,
            (int(enemy.x), int(enemy.y)),
            23
        )

    pygame.draw.rect(
        screen,
        (40, 40, 40),
        (20, 20, 250, 25)
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (20, 20, int(250 * health / 100), 25)
    )

    screen.blit(
        FONT.render(f"Score: {score}", True, WHITE),
        (20, 60)
    )

    screen.blit(
        FONT.render("WASD = Move   Mouse = Shoot", True, WHITE),
        (20, 100)
    )

    pygame.display.flip()

# Game over
screen.fill(BLACK)

text = BIG.render("GAME OVER", True, RED)
screen.blit(text, text.get_rect(center=(WIDTH // 2, 300)))

score_text = FONT.render(f"Score: {score}", True, WHITE)
screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 390)))

pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
