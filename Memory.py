# implementation of card game - Memory

import simplegui
import random

cardlist = []
exposed = [False] * 16
firstchoice = int
secondchoice = int
turns = 0

cardlist = range(0, 8) + range(0,8)
random.shuffle(cardlist)

# helper function to initialize globals
def new_game():
    global state, turns, exposed, firstchoice, secondchoice
    state = 0
    exposed = [False] * 16
    firstchoice = int
    secondchoice = int
    turns = 0
    label.set_text("Turns = 0")
    random.shuffle(cardlist)
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, firstchoice, secondchoice, turns
    cardindex = pos[0] // 50

    if state == 0:
        firstchoice = cardindex
        exposed[cardindex] = True
        state = 1
    elif state == 1:
        if exposed[cardindex]:
            return
        else:
            secondchoice = cardindex
            exposed[cardindex] = True
            turns += 1
            label.set_text("Turns = " + str(turns))
            state = 2

    else:
        if exposed[cardindex]:
            return
        if cardlist[firstchoice] == cardlist[secondchoice]:
            exposed[firstchoice] = True
            exposed[secondchoice] = True
            exposed[cardindex] = True
            firstchoice = cardindex

        else:
            exposed[firstchoice] = False
            exposed[secondchoice] = False
            exposed[cardindex] = True
            firstchoice = cardindex


        state = 1

    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    x = 0
    cardwidth = 50
    cardheight = 100
    for i in range(0,16):
        if exposed[i] is False:
            canvas.draw_polygon([(cardwidth*i, 0),
                (cardwidth*i + cardwidth, 0),
                (cardwidth*i + cardwidth, cardheight), 
                (cardwidth*i, cardheight)],
                5, "Blue", "Green")
        else:
            canvas.draw_text(str(cardlist[i]), (x, 85), 95, 'White')
        x = x + 50


# create frame and add a button and labels

frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
