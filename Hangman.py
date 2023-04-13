#hide code
from tracemalloc import start
import turtle
import random
import time
from tkinter import *
import tkinter as tk

def get_words():
    global file_name
    global random_words
    random_words = []
    file = open(file_name, "r") 

    for line in file:
        word = ""
        index = 0
        while(index < len(line) - 1):
            word += line[index]
            index = index + 1 
            word = word.lower()
        if(len(word) > 5 and len(word) < 10):
            random_words.append(word)

    file.close()

def starting_spot(x,y):
    hangman.pensize(5)
    hangman.penup()
    hangman.goto(x-50,y+100)
    hangman.pendown()

def create_base():
    starting_spot(-50,50)
    hangman.pendown()
    hangman.color("black")
    hangman.setheading(90)
    hangman.forward(50)
    hangman.right(90)
    hangman.forward(200)
    hangman.right(90)
    hangman.forward(300)
    hangman.right(90)
    hangman.forward(150)
    hangman.right(180)
    hangman.forward(300)

def head():
    starting_spot(-50,-10)
    hangman.circle(30)

def body():
    starting_spot(-50,-10)
    hangman.setheading(270)
    hangman.forward(80)

def leg(side):
    starting_spot(-50,-90)
    if(side == 3):
        hangman.setheading(225)
        hangman.forward(65)
    elif(side == 4):
        hangman.setheading(315)
        hangman.forward(65)
        
def arm(side):
    starting_spot(-50,-10)
    if(side == 5):
        hangman.setheading(225)
        hangman.forward(65)
    elif(side == 6):
        hangman.setheading(315)
        hangman.forward(65)

def eye(side):
    if(side == 7):
        starting_spot(-63,23)
        hangman.color("blue")
        hangman.begin_fill()
        hangman.circle(5)
        hangman.end_fill()
    elif(side == 8):
        starting_spot(-43,23)
        hangman.color("blue")
        hangman.begin_fill()
        hangman.circle(5)
        hangman.end_fill()

def mouth():
    starting_spot(-40,0)
    hangman.setheading(90)
    hangman.color("red")
    hangman.circle(10,180)

def blanks(word):
    starting_spot(int(len(word)*(-60)) , -350)
    hangman.pendown()
    hangman.color("black")
    hangman.setheading(0)
    hangman.pendown()
    for letter in word:
        hangman.pendown()
        hangman.forward(60)
        hangman.penup()
        hangman.forward(60)
        hangman.pendown()
    pen.goto(int(len(word)*(-60)) + 20 , -345)

def letter_bank():
    global buttons , associations
    x = -650
    canvas = wn.getcanvas()
    index = 0
    for letters in alphabet:
        buttons.append(Button(canvas.master , text = letters , font = ("Arial" , 24 , "bold") , command = lambda c = index: check_guess(c)))
        canvas.create_window(x , 330 , window = buttons[index])
        associations.append(letters)
        x = x + 50
        index = index + 1

def check_guess(index):
    global buttons , associations , word , body_parts , correct_letters , replay , win
    guess = buttons[index].cget('text')
    buttons[index].destroy()
    if(guess in word):
        for index in range(len(word)):
            if(word[index]==guess):
                correct_letters = correct_letters + 1
                pen2.goto(int((len(word)+1)*(-60)) + (120*index) + 30 , -250)
                pen2.write(guess , font = ('Arial' , 40 , 'bold'))
        if(correct_letters == len(word)):
            for button in buttons:
                button.destroy()
            pen.goto(0 , 225)
            pen.clear()
            pen.write("YOU WIN!" , font = ('Arial' , 80 , 'bold') , align = 'center')
            
            #if(body_parts == 0):
                
            win = True
            replay = Button(canvas.master , text = "Play again" , font = ("Arial" , 24 , "bold") , command = play)
            canvas.create_window(250 , 0 , window = replay)
    else:
        body_parts = body_parts + 1
        if(body_parts == 1):
            head()
        elif(body_parts == 2):
            body()
        elif(body_parts == 3):
            leg(3)
        elif(body_parts == 4):
            leg(4)
        elif(body_parts == 5):
            arm(5)
        elif(body_parts == 6):
            arm(6)
        elif(body_parts == 7):
            eye(7)
        elif(body_parts == 8):
            eye(8)
        elif(body_parts == 9):
            mouth()
            for button in buttons:
                button.destroy()
            
            pen.clear()
            pen.goto(0 , 225)
            win = True
            pen.write("YOU LOSE!\nThe word was " + word , font = ('Arial' , 50 , 'bold') , align = 'center')
            replay = Button(canvas.master , text = "Play again" , font = ("Arial" , 24 , "bold") , command = play)
            canvas.create_window(250 , 0 , window = replay)
        
def play(): 
    global win , replay , word , wn , buttons , associations , alphabet , guesses , correct_letters , body_parts , file_name , random_words , hangman , pen , canvas 
    replay.destroy()
    wn.clear()
    hangman.forward(1)
    win = False
    random_words = []
    buttons = []
    associations = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    word = ""
    guesses = ""
    correct_letters = 0
    body_parts = 0
    file_name = "Random Words.txt"
    create_base()
    get_words()
    word = random.choice(random_words)
    #write_encryption(word)
    #countdown(60)
    blanks(word)
    letter_bank()

def encrypt(word):
    encryption = ""
    full_encryption = ""
    num_cos = -1
    num_vowels = -1
    consonants = "bcdfghjklmnpqrstvwxz"
    vowels = "aeiouy"
    for letter in word:
        if(letter in vowels):
            num_cos += 1
            encryption = encryption + consonants[num_cos%len(consonants)]
        else:
            num_vowels += 1
            encryption = encryption + vowels[num_vowels%len(vowels)]
    
    for letter in word:
        eight_bit = str("{0:b}".format(ord(letter)))
        while (len(eight_bit) < 8):
            eight_bit = '0' + eight_bit
        full_encryption = full_encryption + eight_bit + " "
    return full_encryption

def write_encryption(word):
    pen.pensize(5)
    pen.penup()
    pen.goto(int(len(word)*(-70)) - 50,325)
    pen.write(encrypt(word) , font = ("Arial" , 24 , "bold"))

def countdown(t):
    global timer
    timer.goto(270,200)
    while t and not win:
        timer.clear()
        mins, secs = divmod(t, 60)
        clock = '{:02d}:{:02d}'.format(mins, secs)
        timer.write(clock , font = ("Arial" , 40 , "bold"))
        time.sleep(0.25)
        t -= 1
    timer.clear()
    

# Initializing turtles
win = False
hangman = turtle.Turtle()
hangman.hideturtle()
hangman.speed(0)
hangman.color("black")
hangman.pendown()

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.color("black")
pen.penup()

pen2 = turtle.Turtle()
pen2.hideturtle()
pen2.speed(0)
pen2.color("black")
pen2.penup()

timer = turtle.Turtle()
timer.hideturtle()
timer.speed(0)
timer.color("black")
timer.penup()

wn = turtle.Screen()
wn.screensize(1200,1000)
wn.bgcolor("white")



canvas = wn.getcanvas()
replay = Button(canvas.master , text = "PLAY" , font = ("Arial" , 96 , "bold") , command = play)
canvas.create_window(0 , 0 , window = replay)

thing = Label(canvas.master , text = "HIIIII" , font = ("Arial" , 96 , "bold"))
canvas.create_window(0 , 0 , window = thing)
time.sleep(3)
thing.destroy()

wn.mainloop()
