import pygame
import sys
import random

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breakout Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
pink = (255, 105, 180)  # Pink color for the paddle
orange = (255, 165, 0)  # Orange color for the bricks

# Paddle settings
paddle_width = 100
paddle_height = 10
paddle_speed = 10
paddle = pygame.Rect(350, 550, paddle_width, paddle_height)

# Ball settings
ball_size = 20  # Increased ball size
ball_speed = [5, -5]
ball = pygame.Rect(390, 530, ball_size, ball_size)  # Adjusted position

# Brick settings
brick_width = 70
brick_height = 20
brick_padding = 10
brick_offset_x = 35
brick_offset_y = 45

# Game variables
score = 0
lives = 3
level = 1
font = pygame.font.SysFont(None, 36)

# Function to create bricks
def create_bricks(level):
    brick_rows = 4 + level
    brick_cols = 9
    bricks = []
    for i in range(brick_rows):
        for j in range(brick_cols):
            if random.choice([True, False]):
                brick_x = brick_offset_x + j * (brick_width + brick_padding)
                brick_y = brick_offset_y + i * (brick_height + brick_padding)
                bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))
    return bricks

def game_over_screen():
    screen.fill(black)
    game_over_text = font.render("Game Over", True, white)
    score_text = font.render(f"Final Score: {score}", True, white)
    restart_text = font.render("Press R to Restart or Q to Quit", True, white)
    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 250))
    screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    return False

def level_up_screen():
    screen.fill(black)
    level_up_text = font.render(f"Level {level} complete!", True, white)
    continue_text = font.render("Press Space to continue", True, white)
    screen.blit(level_up_text, (screen.get_width() // 2 - level_up_text.get_width() // 2, 250))
    screen.blit(continue_text, (screen.get_width() // 2 - continue_text.get_width() // 2, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    global score, lives, level, ball_speed, ball, paddle

    score = 0
    lives = 3
    level = 1
    paddle = pygame.Rect(350, 550, paddle_width, paddle_height)
    ball = pygame.Rect(390, 530, ball_size, ball_size)  # Adjusted position
    ball_speed = [5, -5]
    bricks = create_bricks(level)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed      
        if keys[pygame.K_RIGHT] and paddle.right < screen.get_width():
            paddle.left += paddle_speed  

        ball.left += ball_speed[0]
        ball.top += ball_speed[1]

        if ball.left <= 0 or ball.right >= screen.get_width():
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]
        
        for brick in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove(brick)
                score += 10
        
        if not bricks:
            level += 1
            level_up_screen()
            bricks = create_bricks(level)
            ball.left = 390
            ball.top = 530
            ball_speed = [5, -5]
            paddle.left = 350

        if ball.top >= screen.get_height():
            lives -= 1
            if lives == 0:
                running = False
            else:
                ball.left = 390
                ball.top = 530
                ball_speed = [5, -5]
                paddle.left = 350
        
        screen.fill(black)
        pygame.draw.rect(screen, pink, paddle)  # Paddle is now pink
        pygame.draw.ellipse(screen, white, ball)

        for brick in bricks:
            pygame.draw.rect(screen, orange, brick)  # Bricks are now orange
        
        score_text = font.render(f"Score: {score}", True, white)
        lives_text = font.render(f"Lives: {lives}", True, white)
        level_text = font.render(f"Level: {level}", True, white)

        screen.blit(score_text, (20, 10))
        screen.blit(lives_text, (700, 10))
        screen.blit(level_text, (360, 10))

        pygame.display.flip()
        clock.tick(60)

    if game_over_screen():
        main()

main()
pygame.quit()
