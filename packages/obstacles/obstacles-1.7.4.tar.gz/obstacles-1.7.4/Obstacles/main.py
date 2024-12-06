import turtle
import random
import time

# Sprite class that inherits from Turtle
class Sprite(turtle.Turtle):
    def __init__(self, color, shape, x, y, stride=20):
        super().__init__()
        self.color(color)
        self.shape(shape)
        self.penup()
        self.goto(x, y)
        self.stride = stride
        self.direction = random.choice(['up', 'down', 'left', 'right'])
# Movement methods for player control
    def move_left(self):
        self.setx(self.xcor() - self.stride)

    def move_right(self):
        self.setx(self.xcor() + self.stride)

    def move_up(self):
        self.sety(self.ycor() + self.stride)

    def move_down(self):
        self.sety(self.ycor() - self.stride)
# Method to set direction for obstacles
    def set_move(self):
        if self.xcor() >= 340 or self.xcor() <= -340:
            self.direction = 'left' if self.direction == 'right' else 'right'
        if self.ycor() >= 340 or self.ycor() <= -340:
            self.direction = 'down' if self.direction == 'up' else 'up'

    # Method to make a step based on the current direction
    def make_step(self):
        self.set_move()
        if self.direction == 'up':
            self.sety(self.ycor() + self.stride)
        elif self.direction == 'down':
            self.sety(self.ycor() - self.stride)
        elif self.direction == 'left':
            self.setx(self.xcor() - self.stride)
        elif self.direction == 'right':
            self.setx(self.xcor() + self.stride)

    # Collision detection method
    def is_collide(self, other):
        return self.distance(other) < 20
    
    def player_checkpoint(self, checkpoint, checkpoint_set):
        if not checkpoint_set:
            checkpoint.goto(self.xcor(), self.ycor())
            checkpoint.showturtle()
            checkpoint_set = True


def obstacles_game():
    # Game setup
    screen = turtle.Screen()
    screen.setup(width=700, height=700)
    screen.tracer(0)  # Disable automatic updates

    # Filling the Background with Solid Color
    turtle.hideturtle()
    turtle.color('whitesmoke')
    turtle.begin_fill()
    turtle.goto(turtle.xcor(), -500)
    turtle.circle(500)
    turtle.end_fill()

    # Player, target, and obstacles
    player = Sprite('mediumblue', 'turtle', 0, 0, 25)
    target = Sprite('forestgreen', 'circle', random.randint(-340, 340), random.randint(-340, 340))
    obstacles = [Sprite('red', 'square', random.randint(-340, 340), random.randint(-340, 340), stride=15) for _ in range(3)]
    checkpoint = Sprite('mediumseagreen', 'square', 0, 0, 0)
    checkpoint.hideturtle()

    # Score and game state
    score = 0
    #checkscore = 0
    game_over = False
    checkpoint_set = False

    # Keyboard bindings
    screen.listen()
    screen.onkey(player.move_left, 'Left')
    screen.onkey(player.move_right, 'Right')
    screen.onkey(player.move_up, 'Up')
    screen.onkey(player.move_down, 'Down')
    screen.onkey(player.checkpoint(checkpoint, checkpoint_set), 'space')

    # Main game loop
    while not game_over:
        screen.update()
        time.sleep(0.1)

        # Random Player Colors
        #randomcolor = random.choice(['crimson', 'forestgreen', 'mediumblue', 'gold', 'purple', 'turquoise',
                                    # 'darkred', 'darkgreen', 'darkblue', 'darkgoldenrod', 'indigo', 'darkturquoise'])

        # Move obstacles
        for obstacle in obstacles:
            obstacle.make_step()

        # Check collision with target
        if player.is_collide(target):
            score += 1
            #checkscore += 1
            #if checkscore == 3:
            #    checkscore = 0
            print('Score:', score)
            for obstacle in obstacles:
                obstacle.hideturtle()
            target.goto(random.randint(-300, 300), random.randint(-300, 300))  # Relocate target
            obstacles = [Sprite('red', 'square', random.randint(-340, 340), random.randint(-340, 340), stride=15) for _ in range(score + 3)]
            

        # Check collision with obstacles
        for obstacle in obstacles:
            if checkpoint_set == False:
                player.goto(checkpoint.xcor(), checkpoint.ycor())
                checkpoint.hideturtle()
                checkpoint_set = False
            else:
                print("Congratulations! You caught", score, 'points!')
                game_over = True
                target.hideturtle()
                time.sleep(1)
                turtle.bye()

    screen.mainloop()

def obstacles_pygame():
    print('Work in progress')