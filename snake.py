#Imports
from tkinter import *
from random import randint

#CONSTANTS
WIN_HEIGHT = 500
WIN_WIDTH = 500

INIT_TIME = 100

SIZE = 20

FOOD_COLOR = 'yellow'

SNAKE_COLOR = 'green'

ROWS = round(WIN_HEIGHT // SIZE)
COLS = round(WIN_WIDTH // SIZE)

#Classes
class Snake():
    def __init__(self,x=0,y=0,speed=SIZE):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = ''
        self.tail = []
        self.image = ''

    def move(self,moveX,moveY):
        self.x += moveX
        self.y += moveY

    def updateImage(self,c):
        c.delete(self.image)
        self.image = c.create_rectangle(self.x,self.y,self.x+SIZE,self.y+SIZE,fill=SNAKE_COLOR)

class SnakeTail():
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.image = ''

    def updateImage(self,c):
        c.delete(self.image)
        self.image = c.create_rectangle(self.x,self.y,self.x+SIZE,self.y+SIZE,fill=SNAKE_COLOR)

class Food():
    def __init__(self,x=0,y=0,image=''):
        self.x = x
        self.y = y
        self.image = ''

    def spawn(self,minX,minY,maxX,maxY):
        self.x = randint(0,COLS-1) * SIZE
        self.y = randint(0,ROWS-1) * SIZE

    def updateImage(self,c):
        c.delete(self.image)
        self.image = c.create_rectangle(self.x,self.y,self.x+SIZE,self.y+SIZE,fill=FOOD_COLOR)

#Functions        
def main():
    if gameRun.get():
        spawn = spawnBody.get()
        if snake.x < 0 or snake.x > WIN_WIDTH - SIZE or snake.y < 0 or snake.y > WIN_HEIGHT - SIZE:
            gameOver()
        else:
            if spawn:
                snake.tail.append(SnakeTail(prevX.get(),prevY.get()))
                spawnBody.set(False)
                snake.tail[-1].image = c.create_rectangle(snake.x,snake.y,snake.x+SIZE,snake.y+SIZE,fill=SNAKE_COLOR)
            if snake.direction == 'n':
                move(snake.image,0,-snake.speed)
                snake.move(0,-snake.speed)
                if snake.y <= 0:
                    snake.direction = ''
            elif snake.direction == 'w':
                move(snake.image,-snake.speed,0)
                snake.move(-snake.speed,0)
                if snake.x <= 0:
                    snake.direction = ''
            elif snake.direction == 's':
                move(snake.image,0,snake.speed)
                snake.move(0,snake.speed)
                if snake.y >= WIN_HEIGHT - SIZE:
                    snake.direction = ''
            elif snake.direction == 'e':
                move(snake.image,snake.speed,0)
                snake.move(snake.speed,0)
                if snake.x >= WIN_WIDTH - SIZE:
                    snake.direction = ''
            if hitDetect(snake,food):
                score.set(score.get()+1)
                spawnFood()
                spawnBody.set(True)
                tempTime = time.get()
                time.set(tempTime - round(tempTime * 0.1))
            i = len(snake.tail)- 1
            while i >= 0:
                if hitDetect(snake,snake.tail[i]):
                    gameOver()
                    i = -1
                else:
                    tempX = prevX.get()
                    tempY = prevY.get()
                    prevX.set(snake.tail[i].x)
                    prevY.set(snake.tail[i].y)
                    snake.tail[i].x = tempX
                    snake.tail[i].y = tempY
                    snake.tail[i].updateImage(c)
                    i -= 1
            prevX.set(snake.x)
            prevY.set(snake.y)
            root.after(time.get(),main)

#Moves snake
def move(img,moveX,moveY):
    c.move(img,moveX,moveY)
    c.update()

def hitDetect(obj1,obj2):
    hit = False
    if obj1.x == obj2.x and obj1.y == obj2.y:
        hit = True
    return hit

def keyPressed(event):
    if event.char == 'w':
        if len(snake.tail) == 0:
            snake.direction = 'n'
        elif snake.tail[0].y - snake.y < SIZE and snake.x != snake.tail[0].x:
            snake.direction = 'n'
    elif event.char == 'a':
        if len(snake.tail) == 0:
            snake.direction = 'w'
        elif snake.x - snake.tail[0].x < SIZE and snake.y != snake.tail[0].y:
            snake.direction = 'w'
    elif event.char == 'd':
        if len(snake.tail) == 0:
            snake.direction = 'e'
        elif snake.x - snake.tail[0].x < SIZE and snake.y != snake.tail[0].y:
            snake.direction = 'e'
    elif event.char == 's':
        if len(snake.tail) == 0:
            snake.direction = 's'
        elif snake.y - snake.tail[0].y < SIZE and snake.x != snake.tail[0].x:
            snake.direction = 's'

def spawnFood():
    food.spawn(2,477,2,477)
    food.updateImage(c)

def gameOver():
    gameRun.set(False)
    isRetry.set(True)
    for i in range(len(snake.tail)):
        c.delete(snake.tail[i].image)
    snake.tail = []
    c.itemconfigure(snake.image,state='hidden')
    c.itemconfigure(food.image,state = 'hidden')
    if score.get() > highscore.get():
        highscore.set(score.get())
    text.set("GAME OVER!\nScore: " + str(score.get()) + "\n High Score: " + str(highscore.get()) + "\n\nClick below\nto retry.")
    lblGameOver.place(x=110,y=50)

def leftClick(event):
    if not gameRun.get() and not isRetry.get():
        start()
    elif isRetry.get():
        lblGameOver.place_forget()
        lblStart.place(x=30,y=50)
        isRetry.set(False)

def start():
    gameRun.set(True)
    snake.direction = ""
    snake.x = 20
    snake.y = 20
    score.set(0)
    time.set(INIT_TIME)
    c.itemconfigure(snake.image,state = 'normal')
    c.itemconfigure(food.image,state = 'normal')
    lblStart.place_forget()
    snake.updateImage(c)
    food.spawn(2,477,2,477)
    food.updateImage(c)
    main()

#====================
#Main
#====================
root = Tk()
root.title("Snake")
root.minsize(WIN_WIDTH,WIN_HEIGHT)
root.maxsize(WIN_WIDTH,WIN_HEIGHT)

#Game variables
isRetry = BooleanVar()
isRetry.set(False)
gameRun = BooleanVar()
gameRun.set(False)
spawnBody = BooleanVar()
spawnBody.set(False)
score = IntVar()
highscore = IntVar()
highscore.set(0)

c = Canvas(root,width=WIN_WIDTH - 3,height=WIN_HEIGHT - 3)
c.bind("<Key>",keyPressed)
c.bind("<Button-1>",leftClick)
c.pack()
c.focus_set()

#Start
lblStart = Label(c,text="Don't Touch The Walls!\n\nControl Keys: WASD\n\nClick below to start",font=('Arial','30','bold'))
lblStart.place(x=30,y=50)

#Game Over
text = StringVar()
lblGameOver = Label(c,textvariable=text,font=('Arial','30','bold'))

snake = Snake(20,20)
snake.image = c.create_rectangle(snake.x,snake.y,snake.x+SIZE,snake.y+SIZE,fill=SNAKE_COLOR,state='hidden')

prevX = IntVar()
prevY = IntVar()
time = IntVar()

food = Food()
food.spawn(2,477,2,477)
food.image = c.create_rectangle(food.x,food.y,food.x+SIZE,food.y+SIZE,fill=FOOD_COLOR,state='hidden')
root.mainloop()
