import random
import turtle
import time
import math
import os

SAVE_FILE = "balance.txt"

def load_balance():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return int(f.read())
    return 1000

def save_balance(balance):
    with open(SAVE_FILE, "w") as f:
        f.write(str(balance))

class Coin(turtle.Turtle):
    def __init__(self, x, y, size=10):
        super().__init__()
        self.shape("circle")
        self.color("gold")
        self.shapesize(size / 20)
        self.penup()
        self.goto(x, y)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(5, 12)
        self.gravity = 0.3
        self.floor = -220
        self.trails = [] 
        self.showturtle()

    def move(self):
        x, y = self.position()
        self.goto(x + self.vx, y + self.vy)
        self.vy -= self.gravity

        if y + self.vy < self.floor:
            self.vy *= -0.6
            self.vx *= 0.9

        if random.random() < 0.05:
            self.color("yellow")
        else:
            self.color("gold")

        self.create_trail(x, y)

    def create_trail(self, x, y):
        trail = turtle.Turtle()
        trail.hideturtle()
        trail.shape("circle")
        trail.color("orange")
        trail.shapesize(0.3)
        trail.penup()
        trail.goto(x, y)
        trail.stamp()
        self.trails.append((trail, time.time()))

    def update_trails(self, lifetime=0.5):
        current_time = time.time()
        for t in self.trails[:]:
            trail_turtle, t_time = t
            if current_time - t_time > lifetime:
                trail_turtle.clear()
                self.trails.remove(t)

    def hide_with_trails(self):
        for trail_turtle, _ in self.trails:
            trail_turtle.clear()
        self.trails.clear()
        self.hideturtle()

class RedChip(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.shapesize(0.8)
        self.penup()
        self.goto(x, y)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-8, -3)
        self.rotation = random.uniform(-15, 15)
        self.showturtle()
    
    def fall(self):
        x, y = self.position()
        self.goto(x + self.vx, y + self.vy)
        self.vy -= 0.2 
        self.left(self.rotation)
        
        if y < -200:
            self.color("dark red")

class SmokeParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(2, 4)
        self.life = 1.0
        self.circles = []
        
        for i in range(6):
            circle = turtle.Turtle()
            circle.shape("circle")
            circle.color("gray")
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            size = random.uniform(0.4, 0.6)
            circle.shapesize(size)
            circle.penup()
            circle.goto(x + offset_x, y + offset_y)
            circle.showturtle()
            self.circles.append({
                'turtle': circle,
                'offset_x': offset_x,
                'offset_y': offset_y,
                'base_size': size
            })
    
    def rise(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 0.015
        
        for circle_data in self.circles:
            circle = circle_data['turtle']
            
            new_x = self.x + circle_data['offset_x']
            new_y = self.y + circle_data['offset_y']
            circle.goto(new_x, new_y)
            
            if self.life > 0:
                growth = (1 - self.life) * 1.5
                new_size = circle_data['base_size'] + growth
                circle.shapesize(new_size)
                
                if self.life > 0.7:
                    circle.color("gray")
                elif self.life > 0.4:
                    circle.color("light gray")
                else:
                    circle.color("white smoke")
    
    def hide(self):
        for circle_data in self.circles:
            circle_data['turtle'].hideturtle()

def coin_explosion(screen, center_x=0, center_y=0, num_coins=30, coin_size=10, duration=3):

    coins = [Coin(center_x, center_y, coin_size) for _ in range(num_coins)]
    start_time = time.time()

    while time.time() - start_time < duration:
        for coin in coins:
            coin.move()
            coin.update_trails()
        screen.update()

    for coin in coins:
        coin.hide_with_trails()
    screen.update()

def roulette_lose_animation(screen, duration=4, smoke_count=20, smoke_spread=300):

    screen.tracer(0)
    
    line = turtle.Turtle()
    line.hideturtle()
    line.speed(0)
    line.penup()
    line.pensize(5)
    line.color("dark red")
    
    ring = turtle.Turtle()
    ring.hideturtle()
    ring.speed(0)
    ring.penup()
    ring.color("dark red")
    ring.pensize(5)
    ring.goto(0, -120)
    ring.pendown()
    ring.circle(120)
    ring.penup()
    
    text = turtle.Turtle()
    text.hideturtle()
    text.penup()
    
    chips = []
    smoke = []
    
    start = time.time()
    angle = 0
    frame = 0
    
    while time.time() - start < duration:
        line.clear()
        text.clear()
        
        if frame % 3 == 0 and len(chips) < 30:
            chip = RedChip(random.randint(-300, 300), 400)
            chips.append(chip)
        
        if frame % 5 == 0 and len(smoke) < smoke_count:
            spawn_x = random.randint(-smoke_spread, smoke_spread)
            particle = SmokeParticle(spawn_x, -250)
            smoke.append(particle)
        
        for chip in chips[:]:
            chip.fall()
            if chip.ycor() < -300:
                chip.hideturtle()
                chips.remove(chip)
        
        for particle in smoke[:]:
            particle.rise()
            if particle.life <= 0:
                particle.hide()
                smoke.remove(particle)

        for spoke in range(8):
            spoke_angle = angle + (spoke * 45) 
            
            line.goto(0, 0)
            line.setheading(spoke_angle)
            line.pendown()
            line.forward(120)
            line.penup()
            
            end_x = 120 * math.cos(math.radians(spoke_angle))
            end_y = 120 * math.sin(math.radians(spoke_angle))
            
            line.goto(end_x, end_y)
            line.pendown()
            line.fillcolor("dark red")
            line.begin_fill()
            line.circle(10)
            line.end_fill()
            line.penup()
        
        pulse = abs(math.sin(time.time() * 5))
        size = int(32 + pulse * 8)
        
        text.goto(0, 50)
        text.color("red")
        text.write("YOU LOSE", align="center", font=("Arial", size, "bold"))
        
        angle += 8
        frame += 1
        screen.update()
        time.sleep(0.03)
    
    line.clear()
    ring.clear()
    text.clear()
    for chip in chips:
        chip.hideturtle()
    for particle in smoke:
        particle.hide()
    
    text.goto(0, 0)
    text.color("dark red")
    text.write("BETTER LUCK NEXT TIME", align="center", font=("Arial", 28, "bold"))
    screen.update()

def draw_roullet(screen, roll_number):
    screen.bgcolor("darkgreen")
    screen.tracer(0)
    radius = 200
    
    root = screen.getcanvas().winfo_toplevel()
    root.attributes('-topmost', 1)
    root.update()
    root.attributes('-topmost', 0)

    pointer = turtle.Turtle()
    pointer.hideturtle()
    pointer.speed(0)
    pointer.color("grey")
    pointer.width(4)
    pointer.penup()
    pointer.goto(0, radius + 10)
    pointer.pendown()
    pointer.goto(0, radius - 10)

    spoke_count = 37
    angle_step = 360 / spoke_count
    ROULETTE_ORDER = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,
                    16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
    RED_NUMS = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    BLACK_NUMS = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

    wheel = turtle.Turtle()
    wheel.hideturtle()
    wheel.speed(0)
    wheel.penup()

    number_writer = turtle.Turtle()
    number_writer.hideturtle()
    number_writer.penup()
    number_radius = radius - 40

    def draw_wheel(rotation):
        wheel.clear()
        number_writer.clear()
        for i, num in enumerate(ROULETTE_ORDER):
            color = "green" if num == 0 else "red" if num in RED_NUMS else "black"
            start_angle = i * angle_step + rotation
            wheel.penup()
            wheel.goto(0, -radius)
            wheel.setheading(0)
            wheel.pendown()
            wheel.pensize(3)
            wheel.pencolor("gold")
            wheel.circle(radius)
            wheel.penup()
            wheel.goto(0, 0)
            wheel.pendown()
            wheel.setheading(start_angle)
            wheel.fillcolor(color)
            wheel.begin_fill()
            wheel.forward(radius)
            wheel.left(90)
            wheel.circle(radius, angle_step)
            wheel.left(90)
            wheel.forward(radius)
            wheel.end_fill()

            mid_angle = start_angle + angle_step / 2
            rad = math.radians(mid_angle)
            y_offset = -10
            x = number_radius * math.cos(rad)
            y = number_radius * math.sin(rad) + y_offset
            
            number_writer.goto(x, y)
            number_writer.color("white" if num == 0 else "black" if color == "red" else "white")
            number_writer.write(num, align="center", font=("Arial", 12, "bold"))

    final_index = ROULETTE_ORDER.index(roll_number)
    final_rotation = 90 - (final_index * angle_step + angle_step / 2)

    total_spins = 5  
    total_rotation = 360 * total_spins + final_rotation
    steps = 100
    for i in range(steps):
        t = i / steps
        easing = 1 - (1 - t) ** 3 
        rotation = total_rotation * easing
        draw_wheel(rotation)
        screen.update()
        time.sleep(0.02)

    draw_wheel(final_rotation)
    screen.update()

    writer = turtle.Turtle()
    writer.hideturtle()
    writer.color("white")
    writer.goto(0, -radius - 50)
    writer.write(f"Rolled: {roll_number}", align="center", font=("Arial", 24, "bold"))
    screen.update()

def show_message(screen, msg, y_offset=260):
    msg_writer = turtle.Turtle()
    msg_writer.hideturtle()
    msg_writer.penup()
    msg_writer.color("white")
    msg_writer.goto(0, y_offset)
    msg_writer.write(msg, align="center", font=("Arial", 20, "bold"))
    screen.update()

def main():
    print("Welcome to Roulette!")
    
    balance = load_balance()
    amount = int(input("Enter the amount to bet: "))
    bet = input("Bet on (num, red, black, odd, even, 1-18, 19-36, dozens, columns, voisins, tiers, orphelins): ")

  

    RED_NUMS = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    BLACK_NUMS = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

    DOZENS = {
        "1st dozen": range(1, 13),
        "2nd dozen": range(13, 25),
        "3rd dozen": range(25, 37)
    }

    COLUMNS = {
        "1st column": [1,4,7,10,13,16,19,22,25,28,31,34],
        "2nd column": [2,5,8,11,14,17,20,23,26,29,32,35],
        "3rd column": [3,6,9,12,15,18,21,24,27,30,33,36]
    }

    FRENCH_BETS = {
        "voisins": [22,18,29,7,28,12,35,3,26,0,32,15,19,4,21,2,25],
        "tiers": [27,13,36,11,30,8,23,10,5,24,16,33],
        "orphelins": [1,20,14,31,9,17,34,6]
    }

    PAYOUTS = {
        "num": 35,
        "red": 2,
        "black": 2,
        "odd": 2,
        "even": 2,
        "1-18": 2,
        "19-36": 2,
        "1st dozen": 3,
        "2nd dozen": 3,
        "3rd dozen": 3,
        "1st column": 3,
        "2nd column": 3,
        "3rd column": 3,
        "voisins": 3,
        "tiers": 3,
        "orphelins": 3
    }


    number = None
    if bet == "num":
        number = int(input("Enter number (0-36): "))

    roll = random.randint(0, 36)
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.title("roulette")
    print("Rolled:", roll)
    draw_roullet(screen, roll)

    time.sleep(1)

    won = False
    win_amount = 0

    if bet == "num":
        if number == roll:

            win_amount = amount * PAYOUTS['num']
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")
    elif bet == "red":
        if roll in RED_NUMS:
            win_amount = amount * PAYOUTS['red']
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    elif bet == "black":
        if roll in BLACK_NUMS:
            win_amount = amount * PAYOUTS['black']
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    elif bet == "odd":
        if roll % 2 != 0 and roll != 0:
            win_amount = amount * PAYOUTS['odd']
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    elif bet == "even":
        if roll % 2 == 0 and roll != 0:
            win_amount = amount * PAYOUTS['even']
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    elif bet == "1-18":
        if 1 <= roll <= 18:
            win_amount = amount * PAYOUTS['1-18']
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    elif bet == "19-36":
        if 19 <= roll <= 36:
            win_amount = amount * PAYOUTS['19-36']
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    elif bet in DOZENS:
        if roll in DOZENS[bet]:
            win_amount = amount * PAYOUTS[bet]
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    elif bet in COLUMNS:
        if roll in COLUMNS[bet]:
            win_amount = amount * PAYOUTS[bet]
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    elif bet in FRENCH_BETS:
        if roll in FRENCH_BETS[bet]:
            win_amount = amount * PAYOUTS[bet]
            balance += win_amount
            show_message(screen, f"You win! Payout: {win_amount} | Balance: {balance}")
            won = True
        else:
            balance -= amount
            show_message(screen, f"You lose! | Balance: {balance}")

    else:
        show_message(screen, "Invalid bet!")
        turtle.bye()
        return

    save_balance(balance)

    if won:
        time.sleep(1) 
        screen.clearscreen()  
        screen.bgcolor("darkgreen") 
        screen.tracer(0) 
        
        win_text = turtle.Turtle()
        win_text.hideturtle()
        win_text.color("gold")
        win_text.penup()
        win_text.goto(0, 250)
        win_text.write(f"YOU WIN: €{win_amount}", align="center", font=("Arial", 36, "bold"))
        screen.update()
        
        coin_explosion(screen, center_x=0, center_y=0, num_coins=60, coin_size=12, duration=5)
    else:
        time.sleep(1)
        screen.clearscreen()
        screen.bgcolor("black")
        screen.tracer(0)
        
        roulette_lose_animation(screen, duration=5, smoke_count=30, smoke_spread=300)
        
    time.sleep(2)  
    
    try:
        screen.bye()
    except:
        pass

if __name__ == "__main__":
    main()