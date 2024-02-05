import pygame as pg
from random import randint
pg.init()

class Block:
    def __init__(self, x, y, color):
        self.color = color
        self.x = x*CELL_WIDTH
        self.y = y*CELL_HEIGHT
        self.block = pg.Rect(self.x, self.y, CELL_WIDTH, CELL_HEIGHT)

class Snake:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.direction = "right"
        self.snake_body = [Block(self.x-1, self.y-1, self.color), Block(self.x-2,self.y-1, self.color), Block(self.x-3, self.y-1, self.color)]

    def draw_snake(self):
        for body in self.snake_body:
            pg.draw.rect(window, pg.Color(body.color), body.block)
            
    def move_snake(self):
        if self.direction == "right":
            self.snake_body.pop()
            new_head = Block(self.x-1, self.y-1, self.color)
            self.snake_body.insert(0, new_head)
            self.x += 1
            
        if self.direction == "left":
            self.snake_body.pop()
            new_head = Block(self.x-1, self.y-1, self.color)
            self.snake_body.insert(0, new_head)
            self.x -= 1
            
        if self.direction == "up":
            self.snake_body.pop()
            new_head = Block(self.x-1, self.y-1, self.color)
            self.snake_body.insert(0, new_head)
            self.y -= 1
            
        if self.direction == "down":
            self.snake_body.pop()
            new_head = Block(self.x-1, self.y-1, self.color)
            self.snake_body.insert(0, new_head)
            self.y += 1
                                              
class Apple:
    def __init__(self):
        self.x = randint(0, COL-1)
        self.y = randint(0, LINE-1)
        
    def draw_apple(self):
        self.food = Block(self.x, self.y, "red")
        pg.draw.rect(window, pg.Color(self.food.color), self.food.block)   
        
class Game:
    def __init__(self):
        self.snake = Snake("blue", 12, 10)
        self.apple = Apple()
        
    def draw(self):
        self.snake.draw_snake()
        self.apple.draw_apple()
        
    def update(self):
        self.snake.move_snake()
        self.interactions()
        
    def generate_apple(self):
        self.apple = Apple()
    
    def interactions(self):
        snake_head = self.snake.snake_body[0]
        food_block = self.apple.food
        if snake_head.x == food_block.x and snake_head.y == food_block.y:
            self.snake.snake_body.append(food_block)
            self.generate_apple()
            
        for block in self.snake.snake_body:
            if block.x == food_block.x and block.y == food_block.y:
                self.generate_apple()
                
CELL_WIDTH = 30
CELL_HEIGHT = 30

COL = 20
LINE = 20

pg.display.set_caption("snake")
window = pg.display.set_mode([COL*CELL_WIDTH, LINE*CELL_HEIGHT], pg.DOUBLEBUF)
window.fill(pg.Color("green"))

timer = pg.time.Clock()
MOLO = pg.USEREVENT
pg.time.set_timer(MOLO, 120)

def grid():
    for i in range(0, COL):
        for j in range(0, LINE):
            square = pg.Rect(j*CELL_WIDTH, i*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            pg.draw.rect(window, pg.Color("black"), square, 1)

game = Game()
start_time = pg.time.get_ticks()

launched = True
while launched:
    
    current_time = pg.time.get_ticks()
    elapsed_time = current_time - start_time
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            launched = False
        elif game.snake.x == 0 and game.snake.direction == 'left':
            launched = False
        elif game.snake.x == 21 and game.snake.direction == 'right':
            launched = False
        elif game.snake.y == 0 and game.snake.direction == 'up':
            launched = False
        elif game.snake.y == 21 and game.snake.direction == 'down':
            launched = False
            
        for block in game.snake.snake_body[1:len(game.snake.snake_body) - 1]:
            if block.x == game.snake.snake_body[0].x and block.y == game.snake.snake_body[0].y and elapsed_time > 3000:
                launched = False
            
        if event.type == MOLO:
            game.update()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT and game.snake.direction != "left":
                game.snake.direction = "right"
            if event.key == pg.K_LEFT and game.snake.direction != "right":
                game.snake.direction = "left"
            if event.key == pg.K_UP and game.snake.direction != "down":
                game.snake.direction = "up"
            if event.key == pg.K_DOWN and game.snake.direction != "up":
                game.snake.direction = "down"
                
    window.fill(pg.Color("green"))  
    grid()
    game.draw()
    pg.display.update()
    timer.tick(60)
