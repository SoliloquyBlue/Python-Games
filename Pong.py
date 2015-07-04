# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [(WIDTH / 2), (HEIGHT / 2)] 
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
leftscore = 0
rightscore = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    if direction == RIGHT:
        ball_vel = [random.randrange(120, 240) /60, -random.randrange(60, 180)/60]
    else:
        ball_vel = [-random.randrange(120, 240)/60, random.randrange(60, 180)/60]
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global leftscore, rightscore  # these are ints
    leftscore = 0
    rightscore = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel, leftscore, rightscore
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    if ball_pos[1] < 0:
        ball_vel[1] =  -ball_vel[1]
    elif ball_pos[1] > HEIGHT:
        ball_vel[1] =  -ball_vel[1]
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if paddle1_pos-40 <= ball_pos[1] <= paddle1_pos + 40:
            ball_vel[0] = -(ball_vel[0] + ball_vel[0]/10)
            ball_vel[1] = ball_vel[1] + ball_vel[1]/10
        else:
            rightscore = rightscore + 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS):
        if paddle2_pos-40 <= ball_pos[1] <= paddle2_pos + 40:
            ball_vel[0] = -(ball_vel[0] + ball_vel[0]/10)
            ball_vel[1] = ball_vel[1] + ball_vel[1]/10
        else:
            leftscore = leftscore + 1
            spawn_ball(LEFT)
    
    # draw ball
    canvas.draw_circle(ball_pos, 20, 1, "White", "White")
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos <= 40 or paddle1_pos >= HEIGHT - 40:
        paddle1_vel = 0
    elif paddle2_pos <= 40 or paddle2_pos >= HEIGHT - 40:
        paddle2_vel = 0
    
    paddle1_pos = paddle1_pos + paddle1_vel
    paddle2_pos = paddle2_pos + paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos - 40), (8, paddle1_pos - 40), (8, paddle1_pos + 40), (0, paddle1_pos + 40), (0, paddle1_pos - 40)], 1, 'White', 'White')
    canvas.draw_polygon([(592, paddle2_pos - 40), (600, paddle2_pos - 40), (600, paddle2_pos + 40), (592, paddle2_pos + 40), (592, paddle2_pos - 40)], 1, 'White', 'White')
    
    # determine whether paddle and ball collide    
    
    # draw scores
    score = str(leftscore) + " / " + str(rightscore)
    scorehalf = frame.get_canvas_textwidth(score, 50) / 2
    canvas.draw_text(score, (300 - scorehalf, 50), 40, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -0.7
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0.7
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -0.7
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0.7
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

def reset_handler():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart = frame.add_button('Restart', reset_handler)

# start frame
new_game()
frame.start()
