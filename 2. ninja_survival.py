import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Survival")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 38)
BIG = pygame.font.Font(None, 80)

BLACK = (10, 10, 18)
WHITE = (255, 255, 255)
RED = (230, 50, 60)
CYAN = (40, 220, 255)
PURPLE = (170, 70, 255)
GREEN = (50, 220, 100)

player = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

enemies = []
slashes = []

health = 100
score = 0
spawn_timer = 0
attack_timer = 0

running = True

while running:

    dt = clock.tick(60) / 1000

    spawn_timer += dt
    attack_timer -= dt

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE and attack_timer <= 0:

                mouse = pygame.Vector2(pygame.mouse.get_pos())
                direction = mouse - player

                if direction.length():

                    direction.normalize()

                    slashes.append([
                        player.copy(),
                        direction,
                        0.15
                    ])

                    attack_timer = 0.35

    keys = pygame.key.get_pressed()

    movement = pygame.Vector2(
        keys[pygame.K_d] - keys[pygame.K_a],
        keys[pygame.K_s] - keys[pygame.K_w]
    )

    if movement.length():

        movement.normalize()
        player += movement * 350 * dt

    player.x = max(30, min(WIDTH - 30, player.x))
    player.y = max(30, min(HEIGHT - 30, player.y))

    if spawn_timer > 0.6:

        spawn_timer = 0

        enemies.append(
            pygame.Vector2(
                random.choice([
                    random.randint(0, WIDTH),
                    0 if random.random() < .5 else WIDTH
                ]),
                random.randint(0, HEIGHT)
            )
        )

    # Enemy movement
    for enemy in enemies[:]:

        direction = player - enemy

        if direction.length():

            direction.normalize()
            enemy += direction * 120 * dt

        if enemy.distance_to(player) < 35:
            health -= 40 * dt

    # Slash attack
    for slash in slashes[:]:

        slash[2] -= dt

        start = slash[0]
        direction = slash[1]

        end = start + direction * 100

        for enemy in enemies[:]:

            if enemy.distance_to(start) < 100:

                enemies.remove(enemy)
                score += 10

        if slash[2] <= 0:
            slashes.remove(slash)

    if health <= 0:
        running = False

    screen.fill(BLACK)

    # Decorative floor
    for x in range(0, WIDTH, 80):
        pygame.draw.line(
            screen,
            (25, 20, 35),
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, 80):
        pygame.draw.line(
            screen,
            (25, 20, 35),
            (0, y),
            (WIDTH, y)
        )

    # Ninja
    pygame.draw.circle(
        screen,
        CYAN,
        (int(player.x), int(player.y)),
        25
    )

    # Sword slashes
    for slash in slashes:

        start = slash[0]
        end = start + slash[1] * 110

        pygame.draw.line(
            screen,
            WHITE,
            start,
            end,
            10
        )

    # Enemies
    for enemy in enemies:

        pygame.draw.circle(
            screen,
            PURPLE,
            (int(enemy.x), int(enemy.y)),
            22
        )

    # Health
    pygame.draw.rect(
        screen,
        RED,
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
        FONT.render("WASD = Move   SPACE = Sword Attack",
                   True, WHITE),
        (20, 100)
    )

    pygame.display.flip()

screen.fill(BLACK)

game_over = BIG.render("NINJA DEFEATED", True, RED)
screen.blit(
    game_over,
    game_over.get_rect(center=(WIDTH // 2, 300))
)

pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
