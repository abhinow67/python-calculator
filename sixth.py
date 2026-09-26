import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Python Heart")

# Set up the turtle
pen = turtle.Turtle()
pen.color("red")
pen.fillcolor("red")
pen.speed(3)
pen.pensize(3)

# Function to draw the top curves of the heart
def draw_curve():
    for _ in range(200):
        pen.right(1)
        pen.forward(1)

# Drawing the heart
pen.begin_fill()
pen.left(140)
pen.forward(112)

# Left curve
draw_curve()
pen.left(120)

# Right curve
draw_curve()
pen.forward(112)
pen.end_fill()

# Hide turtle and keep window open
pen.hideturtle()
turtle.done()