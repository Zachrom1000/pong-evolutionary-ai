# Run in Python 3.13.8 with pygame 2.1.0

import pygame
import sys
import random
import math


# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 150
left_paddle_speed = 0
right_paddle_speed = 0

# Ball settings
BALL_SIZE = 20

while True:
    ball_speed_x = random.random() * 7 * random.choice([-1, 1])
    if ball_speed_x > 6 or ball_speed_x < -6:
        break
ball_speed_y = math.sqrt(49-ball_speed_x**2) * random.choice([-1, 1])

# Paddle positions
left_paddle = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH-20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball position
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Scores
left_score = 0
right_score = 0
font = pygame.font.SysFont(None, 48)


clock = pygame.time.Clock()
# Variable to control the game speed (frames per second)
game_fps = 60


def draw():
    """
    Draws all game elements (paddles, ball, scores) to the screen and updates the display.
    """
    # Clear the screen by filling it with the background color
    WIN.fill(BLACK)
    # Draw the left paddle
    pygame.draw.rect(WIN, WHITE, left_paddle)
    # Draw the right paddle
    pygame.draw.rect(WIN, WHITE, right_paddle)
    # Draw the ball
    pygame.draw.ellipse(WIN, WHITE, ball)
    # Render the left player's score
    left_text = font.render(str(left_score), True, WHITE)
    # Render the right player's score
    right_text = font.render(str(right_score), True, WHITE)
    # Display the left score on the left side of the screen
    WIN.blit(left_text, (WIDTH//4, 20))
    # Display the right score on the right side of the screen
    WIN.blit(right_text, (WIDTH*3//4, 20))
    # Show info about the F key for speed toggle
    info_font = pygame.font.SysFont(None, 32)
    info_text = info_font.render("Press F for 3x speed, again for 25x, and again for 1x", True, WHITE)
    WIN.blit(info_text, (WIDTH//2 - info_text.get_width()//2, HEIGHT - 40))
    # Update the display with all drawn elements
    pygame.display.flip()

flip = 1
def reset_ball():
    """
    Resets the ball to the center and assigns it a new random velocity.
    """
    global flip
    flip *= -1
    # Reset the ball to the center of the screen
    ball.center = (WIDTH//2, HEIGHT//2)
    left_paddle.centery = HEIGHT//2
    right_paddle.centery = HEIGHT//2
    global right_paddle_speed, left_paddle_speed
    right_paddle_speed = 0
    left_paddle_speed = 0
    global ball_speed_x, ball_speed_y
    # Randomize the ball's horizontal speed, ensuring it's not too slow
    while True:
        ball_speed_x = random.random() * 7 * flip
        if ball_speed_x > 6 or ball_speed_x < -6:
            break
    # Calculate the vertical speed so the total speed is constant, and randomize direction
    ball_speed_y = math.sqrt(49-ball_speed_x**2) * random.choice([-1, 1])


class EvolutionaryAI:
    def __init__(self, ball_x_weight = 0, ball_y_weight = 0, ball_speed_x_weight = 0, ball_speed_y_weight = 0, paddle_y_weight = 0, paddle_speed_weight = 0, points = 0):
        # Initializes the AI with given weights and applies mutation based on rounds survived (mutation decreases with more rounds survived)
        self.points = 1/3 * points
        self.ball_x_weight = self.clamp(self.mutate_weights(ball_x_weight))
        self.ball_y_weight = self.clamp(self.mutate_weights(ball_y_weight))
        self.ball_speed_x_weight = self.clamp(self.mutate_weights(ball_speed_x_weight))
        self.ball_speed_y_weight = self.clamp(self.mutate_weights(ball_speed_y_weight))
        self.paddle_y_weight = self.clamp(self.mutate_weights(paddle_y_weight))
        self.paddle_speed_weight = self.clamp(self.mutate_weights(paddle_speed_weight))

    def determine_movement(self, ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_y, paddle_speed):
        # Determines the paddle movement based on the weighted sum of inputs
        score = (self.ball_x_weight * ball_x +
                 self.ball_y_weight * ball_y +
                 self.ball_speed_x_weight * ball_speed_x +
                 self.ball_speed_y_weight * ball_speed_y +
                 self.paddle_y_weight * paddle_y +
                 self.paddle_speed_weight * paddle_speed)
        if score > 0.1:
            return 1  # Move down
        elif score < -0.1:
            return -1  # Move up
        else:
            return 0  # Stay
        
    def clamp(self, val):
        return max(-1, min(1, val))

    def mutate_weights(self, weight):
        # Weights how much the weight should mutate based on points (more points = less mutation)
        return weight + 1.25 * 1.5**-(1/3*self.points) * random.random() * random.choice([-1, 1])

left_ai = EvolutionaryAI()
right_ai = EvolutionaryAI()

i = 0
while True:
    # Closes window when user clicks the close button 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Press 'F' to toggle between speeds
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if game_fps == 60:
                    game_fps = 60*3
                elif game_fps == 60*3:
                    game_fps = 60*25
                else:
                    game_fps = 60
                  
    # Moves paddles
    if left_paddle.top > 0:
        if left_paddle.bottom < HEIGHT:
            left_paddle.y += left_paddle_speed
        # Prevents paddle from going out of bounds
        else:
            left_paddle.y -= abs(left_paddle_speed) * 1.5
            left_paddle_speed *= 0.25
    else:
        # Prevents paddle from going out of bounds
        left_paddle.y += abs(left_paddle_speed) * 1.5
        left_paddle_speed *= 0.25

    if right_paddle.top > 0:
        if right_paddle.bottom < HEIGHT:
            right_paddle.y += right_paddle_speed
        # Prevents paddle from going out of bounds
        else:
            right_paddle.y -= abs(right_paddle_speed) * 1.5
            right_paddle_speed *= 0.25
    else:
        # Prevents paddle from going out of bounds
        right_paddle.y += abs(right_paddle_speed) * 1.5
        right_paddle_speed *= 0.25

    # Handles paddle movement
    left_movement = left_ai.determine_movement(ball.centerx, ball.centery, ball_speed_x, ball_speed_y, left_paddle.centery, left_paddle_speed)
    right_movement = right_ai.determine_movement(WIDTH-ball.centerx, ball.centery, -ball_speed_x, ball_speed_y, right_paddle.centery, right_paddle_speed)


    # Left paddle
    if left_movement == -1 and left_paddle.top > 10 and abs(left_paddle_speed) < 15:
        if left_paddle_speed > 0:
            left_paddle_speed -= 1
        left_paddle_speed -= 2
    elif left_movement == 1 and left_paddle.bottom < HEIGHT - 10 and abs(left_paddle_speed) < 15:
        if left_paddle_speed < 0:
            left_paddle_speed += 1
        left_paddle_speed += 2
    else:
        left_paddle_speed -= 1/3 * (left_paddle_speed/abs(left_paddle_speed)) if left_paddle_speed != 0 else left_paddle_speed
    # Right paddle
    if right_movement == -1 and right_paddle.top > 10 and abs(right_paddle_speed) < 15:
        if right_paddle_speed > 0:
            right_paddle_speed -= 1
        right_paddle_speed -= 2
    elif right_movement == 1 and right_paddle.bottom < HEIGHT - 10 and abs(right_paddle_speed) < 15:
        if right_paddle_speed < 0:
            right_paddle_speed += 1
        right_paddle_speed += 2
    else:
        right_paddle_speed -= 1/3 * (right_paddle_speed/abs(right_paddle_speed)) if right_paddle_speed != 0 else right_paddle_speed

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collisions
    if ball.top <= 0 and ball_speed_y < 0:
        ball_speed_y *= -1
    if ball.bottom >= HEIGHT and ball_speed_y > 0:
        ball_speed_y *= -1
    if ball.colliderect(left_paddle) and ball_speed_x < 0:
        ball_speed_x *= -1
        ball_speed_y = min(ball_speed_y+left_paddle_speed, 3.5)
        left_ai.points += 1
    if ball.colliderect(right_paddle) and ball_speed_x > 0:
        ball_speed_x *= -1
        ball_speed_y = min(ball_speed_y+right_paddle_speed, 3.5)
        right_ai.points += 1

    # Score
    if ball.left <= 0:
        right_score += 1
        right_ai.points += 7 * (-2**-(right_ai.points/2-1)+2)
        left_ai = EvolutionaryAI(right_ai.ball_x_weight, right_ai.ball_y_weight, right_ai.ball_speed_x_weight, right_ai.ball_speed_y_weight, right_ai.paddle_y_weight, right_ai.paddle_speed_weight, right_ai.points)
        reset_ball()
        i=0
    if ball.right >= WIDTH:
        left_score += 1
        left_ai.points += 7 * (-2**-(left_ai.points/2-1)+2)
        right_ai = EvolutionaryAI(left_ai.ball_x_weight, left_ai.ball_y_weight, left_ai.ball_speed_x_weight, left_ai.ball_speed_y_weight, left_ai.paddle_y_weight, left_ai.paddle_speed_weight, left_ai.points)
        reset_ball()
        i=0

    draw()
    # Resets ball incase of infinite loop
    i += 1
    if i >= 3000:
        reset_ball()
        i = 0
    clock.tick(game_fps)
