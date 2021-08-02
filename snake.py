from turtle import Turtle, Screen
from time import sleep
from random import randint
START_POSITION = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 30
UP = 90
DOWN = 270
LEFT = 0
RIGHT = 180
FONT = ("Courier", 15, "normal")

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)


class Snake:
    powerups_on_board = []

    def __init__(self):
        self.segments = []
        for i in START_POSITION:
            t = Turtle("square")
            t.color("white")
            t.speed(6)
            t.pu()
            t.goto(i)
            self.segments.append(t)
        self.head = self.segments[0]

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].goto(self.segments[i - 1].xcor(), self.segments[i - 1].ycor())
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def give_food(self):
        food = Turtle('circle')
        food.color("white")
        food.pu()
        coord = (randint(-280, 280), randint(-280, 280))
        food.goto(coord)
        return food

    def add_tail(self):
        to = self.segments[len(self.segments) - 1].pos()
        score_board.score += 1
        score_board.update()
        t = Turtle("square")
        t.color("white")
        t.speed(6)
        t.pu()
        t.goto(to)
        self.segments.append(t)

    def give_powerup(self):
        powerup = Turtle('circle')
        self.powerups_on_board.append(powerup)
        powerup.color("red")
        powerup.pu()
        coord = (randint(-280, 280), randint(-280, 280))
        powerup.goto(coord)
        return powerup


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("data.txt", "r") as f:
            self.high_score = int(f.read())
        self.hideturtle()
        self.color("white")
        self.penup()
        self.goto(-270, 250)
        self.write(f"Score: {self.score} | High score = {self.high_score}", align="left", font=FONT)

    def update(self):
        self.clear()
        self.write(f"Score: {self.score} | High score = {self.high_score}", align="left", font=FONT)


snake = Snake()
score_board = Scoreboard()
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Right")
screen.onkey(snake.right, "Left")

food = snake.give_food()
powerup = None
game_is_on = True
while game_is_on:
    screen.update()
    sleep(0.1)
    snake.move()
    # Eat food
    if snake.head.distance(food) < 25:
        snake.add_tail()
        food.reset()
        food.color("white")
        food.pu()
        coord = (randint(-280, 280), randint(-280, 280))
        food.goto(coord)
        if len(snake.segments) % 5 == 0:
            powerup = snake.give_powerup()
    for powerup in snake.powerups_on_board:
        if powerup and snake.head.distance(powerup) < 25:
            snake.add_tail()
            snake.add_tail()
            powerup.goto(600, 600)
            del powerup

    for i in snake.segments[1:]:
        if snake.head.distance(i) <= 10:
            if score_board.score > score_board.high_score:
                with open("data.txt", "w") as f:
                    f.write(f"{score_board.score}")
            game_is_on = False
    if snake.head.xcor() <= -300 or snake.head.xcor() >= 300 or snake.head.ycor() <= -300 or snake.head.ycor() >= 300:
        if score_board.score > score_board.high_score:
            with open("data.txt", "w") as f:
                f.write(f"{score_board.score}")
        game_is_on = False
print(f'You scored: {score_board.score}!')
screen.exitonclick()
