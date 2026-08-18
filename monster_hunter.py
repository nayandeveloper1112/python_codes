import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Hunter")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 38)
BIG = pygame.font.Font(None, 80)

WHITE = (255, 255, 255)
BLACK = (12, 8, 18)
GREEN = (50, 230, 100)
RED = (240, 50, 60)
BLUE = (60, 130, 255)
YELLOW = (255, 220, 40)

player = pygame.Vector2(WIDTH // 2, HEIGHT - 100)

arrows = []
monsters = []

health = 100
score = 0
shoot_timer = 0
spawn_timer = 0

running = True

while running:

    dt = clock.tick(60) / 1000

    shoot_timer -= dt
    spawn_timer += dt

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE and shoot_timer <= 0:

                mouse = pygame.Vector2(
                    pygame.mouse.get_pos()
                )

                direction = mouse - player

                if direction.length():

                    direction.normalize()

                    arrows.append([
                        player.copy(),
                        direction
                    ])

                    shoot_timer = .25

    keys = pygame.key.get_pressed()

    movement = pygame.Vector2(
        keys[pygame.K_d] - keys[pygame.K_a],
        keys[pygame.K_s] - keys[pygame.K_w]
    )

    if movement.length():

        movement.normalize()
        player += movement * 300 * dt

    player.x = max(30, min(WIDTH - 30, player.x))
    player.y = max(30, min(HEIGHT - 30, player.y))

    # Spawn monsters
    if spawn_timer > .8:

        spawn_timer = 0

        monsters.append({
            "pos": pygame.Vector2(
                random.randint(30, WIDTH - 30),
                random.randint(30, HEIGHT - 30)
            ),
            "hp": 30
        })

    # Move monsters
    for monster in monsters:

        pos = monster["pos"]

        direction = player - pos

        if direction.length():

            direction.normalize()
            pos += direction * 80 * dt

        if pos.distance_to(player) < 35:

            health -= 20 * dt

    # Arrows
    for arrow in arrows[:]:

        arrow[0] += arrow[1] * 800 * dt

        if not screen.get_rect().inflate(100, 100).collidepoint(
            arrow[0]
        ):
            arrows.remove(arrow)

    # Hit monsters
    for arrow in arrows[:]:

        for monster in monsters[:]:

            if arrow[0].distance_to(monster["pos"]) < 30:

                monster["hp"] -= 15

                arrows.remove(arrow)

                if monster["hp"] <= 0:

                    monsters.remove(monster)
                    score += 10

                break

    if health <= 0:
        running = False

    screen.fill(BLACK)

    # Ground
    for x in range(0, WIDTH, 80):
        pygame.draw.line(
            screen,
            (25, 18, 35),
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, 80):
        pygame.draw.line(
            screen,
            (25, 18, 35),
            (0, y),
            (WIDTH, y)
        )

    # Player
    pygame.draw.circle(
        screen,
        BLUE,
        (int(player.x), int(player.y)),
        25
    )

    # Arrows
    for arrow in arrows:

        start = arrow[0]
        end = start - arrow[1] * 25

        pygame.draw.line(
            screen,
            YELLOW,
            start,
            end,
            5
        )

    # Monsters
    for monster in monsters:

        pos = monster["pos"]

        pygame.draw.circle(
            screen,
            RED,
            (int(pos.x), int(pos.y)),
            28
        )

        # HP bar
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (pos.x - 25, pos.y - 42, 50, 6)
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (
                pos.x - 25,
                pos.y - 42,
                int(50 * monster["hp"] / 30),
                6
            )
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
        FONT.render(
            f"Monsters defeated: {score // 10}",
            True,
            WHITE
        ),
        (20, 60)
    )

    screen.blit(
        FONT.render(
            "WASD = Move   SPACE = Shoot",
            True,
            WHITE
        ),
        (20, 100)
    )

    pygame.display.flip()

screen.fill(BLACK)

image = BIG.render(
    "HUNTER DEFEATED",
    True,
    RED
)

screen.blit(
    image,
    image.get_rect(
        center=(WIDTH // 2, 300)
    )
)

pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
