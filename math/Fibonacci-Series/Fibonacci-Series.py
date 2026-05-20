import turtle
import math


def print_banner():
    print("=" * 58)
    print("FIBONACCI SERIES GENERATOR")
    print("=" * 58)
    print("Generate Fibonacci numbers and draw a spiral.\n")


def fibonacci(n):
    if n <= 0:
        return []
    if n == 1:
        return [1]
    fib = [1, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib


def get_term_count():
    while True:
        raw_value = input("Enter Fibonacci terms (5-12 recommended): ").strip()
        try:
            term_count = int(raw_value)
            if term_count <= 0:
                print("Please enter a positive number.")
                continue
            return term_count
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def build_layout(fib):
    squares = []

    min_x, max_x = 0, 0
    min_y, max_y = 0, 0

    cx, cy = 0, 0

    for i in range(len(fib)):
        size = fib[i]
        direction = i % 4

        if i == 0:
            x, y = cx, cy
            max_x = max(max_x, x + size)
            max_y = max(max_y, y + size)
        else:
            if direction == 0:
                x = prev_max_x
                y = prev_y + prev_size - size
                max_x = max(max_x, x + size)
            elif direction == 1:
                x = prev_x
                y = prev_max_y
                max_y = max(max_y, y + size)
            elif direction == 2:
                x = prev_x - size
                y = prev_y
                min_x = min(min_x, x)
            else:
                x = prev_x + prev_size - size
                y = prev_y - size
                min_y = min(min_y, y)

        squares.append((x, y, size, direction))

        prev_x, prev_y, prev_size = x, y, size
        prev_max_x, prev_max_y = x + size, y + size

    return squares, min_x, min_y, max_x, max_y

def draw_grid(t, x, y, size):
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.pencolor("#374151")
    t.pensize(1)

    t.pendown()
    for _ in range(4):
        total_drawn = 0
        while total_drawn < size:
            t.forward(min(3, size - total_drawn))
            t.penup()
            t.forward(min(2, size - (total_drawn + 3)))
            t.pendown()
            total_drawn += 5
        t.left(90)
    t.penup()

def draw_smooth_spiral(t, squares, to_screen, scale):
    t.pencolor("#2563eb")
    t.pensize(3)
    t.penup()

    for i, square in enumerate(squares):
        x, y, size, direction = square
        scaled_size = size * scale

        if direction == 0:
            start_x, start_y = x, y
            start_heading = 0
        elif direction == 1:
            start_x, start_y = x + size, y
            start_heading = 90
        elif direction == 2:
            start_x, start_y = x + size, y + size
            start_heading = 180
        else:
            start_x, start_y = x, y + size
            start_heading = 270

        sx, sy = to_screen(start_x, start_y)

        if i == 0:
            t.goto(sx, sy)

        t.setheading(start_heading)
        t.pendown()
        t.circle(scaled_size, 90)
    t.penup()

def fibonacci_spiral(n):
    screen = turtle.Screen()
    screen.setup(1400, 900)
    screen.bgcolor("black")
    screen.title("Perfect Fibonacci Spiral")
    screen.tracer(0)

    grid = turtle.Turtle()
    grid.speed(0)
    grid.hideturtle()

    spiral = turtle.Turtle()
    spiral.speed(0)
    spiral.hideturtle()

    fib = fibonacci(n)
    squares, min_x, min_y, max_x, max_y = build_layout(fib)

    total_w = max_x - min_x
    total_h = max_y - min_y
    padding = 60

    scale = min((1300 - padding * 2) / total_w, (850 - padding * 2) / total_h)

    offset_x = -(min_x + total_w / 2) * scale
    offset_y = -(min_y + total_h / 2) * scale

    def to_screen(x, y):
        return (x * scale + offset_x, y * scale + offset_y)

    for sq in squares:
        x, y, size, _ = sq
        sx, sy = to_screen(x, y)
        draw_grid(grid, sx, sy, size * scale)

    draw_smooth_spiral(spiral, squares, to_screen, scale)

    screen.update()
    screen.exitonclick()


def main():
    print_banner()
    terms = get_term_count()
    fibonacci_spiral(terms)

if __name__ == "__main__":
    main()