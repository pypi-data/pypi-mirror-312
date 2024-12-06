import pygame
import random

def obstacles_game():
    class Sprite():
        def __init__(self, x, y, speed, width, height, color):
            self.x = x
            self.y = y
            self.speed = speed
            self.width = width
            self.height = height
            self.color = color
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        def draw(self, mw):
            pygame.draw.rect(mw, self.color, (self.x, self.y, self.width, self.height))

        def draw_circle(self, mw, radius):
            pygame.draw.circle(mw, self.color, (self.x, self.y), radius)

        def make_step(self):
            if self.direction == 'up':
                self.y -= self.speed
            if self.direction == 'down':
                self.y += self.speed
            if self.direction == 'left':
                self.x -= self.speed
            if self.direction == 'right':
                self.x += self.speed

        def reach_boarders(self):
            if self.y > 700:
                self.direction = 'up'
            if self.y < 0:
                self.direction = 'down'
            if self.x > 700:
                self.direction = 'left'
            if self.x < 0:
                self.direction = 'right'

        def is_collide(self, other, dist):
            if self.x > other.x - dist and self.x < other.x + dist:
                if self.y > other.y - dist and self.y < other.y + dist:
                    return True

    # Initialize Pygame
    pygame.init()

    # Setting up Sprites
    player = Sprite(x=350, y=350, speed=30, width=20, height=20, color=(0, 0, 255))
    target = Sprite(x=random.randint(50, 650), y=random.randint(50, 650), speed=0, width=20, height=20, color=(0, 255, 0))
    obstacles = [Sprite(x=random.randint(50, 650), y=random.randint(50, 650), speed=5, width=20, height=20, color=(255, 0, 0)) for _ in range(3)]

    # Set Command Variables
    score = 0
    lost = False
    window = pygame.display.set_mode((700, 700))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)    
    background = (220, 220, 220)

    # Set Window Title
    pygame.display.set_caption('Obstacles Game')
    
    # The Game Loop
    running = True
    while running:
        window.fill(background)

        # Draw Player
        player.draw(window)

        # Draw Target
        target.draw_circle(window, 12)

        # Draw the TextBox
        if lost == False:
            scoretext = f'Score: {score}'
            scorebox = font.render(scoretext, True, (0, 128, 0))
            window.blit(scorebox, (20, 20))
        else:
            scoretext = 'You lost!'
            font = pygame.font.Font(None, 60)
            scorebox = font.render(scoretext, True, (0, 0, 0))
            window.blit(scorebox, (270, 270))

        for obstacle in obstacles:
            obstacle.draw(window)                               # Draw Obstacles
            obstacle.reach_boarders()                           # Check if obstacles are in the boarders
            obstacle.make_step()                                # Move the obstacles

        if player.is_collide(target, 30) == True:
            target.x = random.randint(50, 650)
            target.y = random.randint(50, 650)
            obstacles.append(Sprite(x=random.randint(50, 650), y=random.randint(50, 650), speed=5, width=20, height=20, color=(255, 0, 0)))
            score += 1

        for obstacle in obstacles:
            if player.is_collide(obstacle, 30) == True:
                background = (255, 50, 50)
                player.speed = 0
                player.color = (220, 220, 220)
                target.color = (220, 220, 220)
                lost = True

                for obstacle in obstacles:
                    obstacle.speed = 0
                    obstacle.color = (220, 220, 220)

        # Keyboard Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.direction = 'up'
                    player.make_step()
                if event.key == pygame.K_DOWN:
                    player.direction = 'down'
                    player.make_step()
                if event.key == pygame.K_LEFT:
                    player.direction = 'left'
                    player.make_step()
                if event.key == pygame.K_RIGHT:
                    player.direction = 'right'
                    player.make_step()

        # Update Display
        pygame.display.update()

        # Tick Rate (48 FPS)
        clock.tick(48)

    # Quit Game
    pygame.quit()