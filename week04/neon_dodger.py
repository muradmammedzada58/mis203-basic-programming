"""
NEON DODGER - a retro arcade mini game
Libraries: pygame (graphics, input, timing) and random (stars, falling blocks)

Controls:  LEFT / RIGHT  or  A / D  to move
           SPACE to restart after a crash,  ESC to quit
"""
import random

import pygame

pygame.init()

# SETTINGS
WIDTH, HEIGHT = 480, 640
BLACK = (8, 6, 20)
CYAN = (0, 255, 240)
PINK = (255, 40, 160)
YELLOW = (255, 230, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON DODGER")
clock = pygame.time.Clock()
font = pygame.font.SysFont("couriernew", 26, bold=True)
big_font = pygame.font.SysFont("couriernew", 54, bold=True)

scanlines = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for y in range(0, HEIGHT, 4):
    pygame.draw.line(scanlines, (0, 0, 0, 70), (0, y), (WIDTH, y))

# Speed of the falling rocks, and the stars in the background (x, y, speed)
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(1, 4)]
         for _ in range(70)]


def draw_text(text, fnt, color, center):
    image = fnt.render(text, True, color)
    screen.blit(image, image.get_rect(center=center))


def new_game():
    player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 40, 40)
    return player, [], 0.0, 4.0  


player, rocks, score, speed = new_game()
high_score = 0
alive = True


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and not alive:
                player, rocks, score, speed = new_game()
                alive = True

    
    screen.fill(BLACK)
    for star in stars:
        star[1] += star[2]
        if star[1] > HEIGHT:
            star[0], star[1] = random.randint(0, WIDTH), 0
        shade = int(star[2] * 50)
        pygame.draw.circle(screen, (shade, shade, 255), (int(star[0]), int(star[1])), 1)

    if alive:
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 7
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 7
        player.clamp_ip(screen.get_rect())

        
        if random.random() < 0.03 + speed * 0.006:
            size = random.randint(25, 60)
            rocks.append(pygame.Rect(random.randint(0, WIDTH - size), -size, size, size))
        for rock in rocks:
            rock.y += speed
        rocks = [rock for rock in rocks if rock.y < HEIGHT]

        
        score += 1 / 6
        speed += 0.002
        if player.collidelist(rocks) != -1:
            alive = False
            high_score = max(high_score, int(score))

    
    for rock in rocks:
        pygame.draw.rect(screen, PINK, rock, 3)
        pygame.draw.rect(screen, (90, 10, 60), rock.inflate(-12, -12))
    if alive:
        ship = [(player.centerx, player.top), (player.left, player.bottom),
                (player.centerx, player.bottom - 10), (player.right, player.bottom)]
        pygame.draw.polygon(screen, CYAN, ship, 3)

    
    draw_text(f"SCORE {int(score):05d}", font, YELLOW, (110, 25))
    draw_text(f"BEST {high_score:05d}", font, CYAN, (WIDTH - 100, 25))
    if not alive:
        draw_text("GAME OVER", big_font, PINK, (WIDTH // 2, HEIGHT // 2 - 20))
        draw_text("press SPACE to retry", font, CYAN, (WIDTH // 2, HEIGHT // 2 + 40))

    screen.blit(scanlines, (0, 0))
    pygame.display.flip()

pygame.quit()
