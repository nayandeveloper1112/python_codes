import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Attack")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 38)
BIG = pygame.font.Font(None, 80)

BLACK = (10, 12, 10)
WHITE = (255, 255, 255)
GREEN = (70, 220, 80)
DARK_GREEN = (30, 120, 40)
RED = (240, 50, 50)
YELLOW = (255, 220, 40)

player = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

zombies = []
bullets = []

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

                if direction.length():

                    direction.normalize()

                    bullets.append([
                        player.copy(),
                        direction
                    ])

                    shoot_timer = .2

    keys = pygame.key.get_pressed()

    movement = pygame.Vector2(
        keys[pygame.K_d] - keys[pygame.K_a],
        keys[pygame.K_s] - keys[pygame.K_w]
    )

    if movement.length():

        movement.normalize()
        player += movement * 350 * dt

    player.x = max(25, min(WIDTH - 25, player.x))
    player.y = max(25, min(HEIGHT - 25, player.y))

    # Spawn zombies
    if spawn_timer > .5:

        spawn_timer = 0

        side = random.randint(0, 3)

        if side == 0:
            pos = pygame.Vector2(random.randint(0, WIDTH), -30)

        elif side == 1:
            pos = pygame.Vector2(random.randint(0, WIDTH), HEIGHT + 30)

        elif side == 2:
            pos = pygame.Vector2(-30, random.randint(0, HEIGHT))

        else:
            pos = pygame.Vector2(WIDTH + 30, random.randint(0, HEIGHT))

        zombies.append(pos)

    # Bullets
    for bullet in bullets[:]:

        bullet[0] += bullet[1] * 900 * dt

        if not screen.get_rect().inflate(100, 100).collidepoint(
            bullet[0]
        ):
            bullets.remove(bullet)

    # Zombies
    for zombie in zombies[:]:

        direction = player - zombie

        if direction.length():

            direction.normalize()
            zombie += direction * 100 * dt

        if zombie.distance_to(player) < 35:

            health -= 40 * dt

    # Collision
    for bullet in bullets[:]:

        for zombie in zombies[:]:

            if bullet[0].distance_to(zombie) < 25:

                bullets.remove(bullet)
                zombies.remove(zombie)

                score += 10
                break

    if health <= 0:
        running = False

    screen.fill(BLACK)

    # Grass
    for x in range(0, WIDTH, 40):
        for y in range(0, HEIGHT, 40):
            pygame.draw.circle(
                screen,
                (15, 35, 15),
                (x, y),
                1
            )

    # Player
    pygame.draw.circle(
        screen,
        YELLOW,
        (int(player.x), int(player.y)),
        25
    )

    # Bullets
    for bullet in bullets:

        pygame.draw.circle(
            screen,
            WHITE,
            (int(bullet[0].x), int(bullet[0].y)),
            5
        )

    # Zombies
    for zombie in zombies:

        pygame.draw.circle(
            screen,
            DARK_GREEN,
            (int(zombie.x), int(zombie.y)),
            24
        )

        pygame.draw.circle(
            screen,
            RED,
            (int(zombie.x - 7), int(zombie.y - 5)),
            4
        )

        pygame.draw.circle(
            screen,
            RED,
            (int(zombie.x + 7), int(zombie.y - 5)),
            4
        )

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
        FONT.render(f"Zombies defeated: {score // 10}",
                   True, WHITE),
        (20, 60)
    )

    screen.blit(
        FONT.render("WASD = Move   Mouse = Shoot",
                   True, WHITE),
        (20, 100)
    )

    pygame.display.flip()

screen.fill(BLACK)

image = BIG.render("ZOMBIES GOT YOU!", True, RED)

screen.blit(
    image,
    image.get_rect(center=(WIDTH // 2, 300))
)

pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
