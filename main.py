import tkinter
import random

# image location
IMGPATH = './img/frog.png'

# initialize window
WINDOW = tkinter.Tk()
WINDOW_WIDTH = 226
WINDOW_HEIGHT = 223
SCREEN_WIDTH = WINDOW.winfo_screenwidth()
SCREEN_HEIGHT = WINDOW.winfo_screenheight()

# make it so theres no background
WINDOW.configure(bg='')

# removes the program header
WINDOW.overrideredirect(True)

# make it so you can exit the program using the escape key
WINDOW.focus_force()
WINDOW.bind("<Escape>", lambda e: WINDOW.destroy())

# set start location and acceleration
x = 100
y = 100
dx = 3
dy = 3

def move_around():
    global x, y, dx, dy

    # update position
    x += dx
    y += dy

    if x <= 0 or x + WINDOW_WIDTH >= SCREEN_WIDTH:
        dx = -dx
    if y <= 0 or y + WINDOW_HEIGHT >= SCREEN_HEIGHT:
        dy = -dy

    WINDOW.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}')

    # call the function again after 50ms
    WINDOW.after(20, move_around)

def main():
    # set the image
    img = tkinter.PhotoImage(file=IMGPATH)

    # make a label
    label = tkinter.Label(image=img, bd=0)
    label.pack()

    move_around()

    # main loop
    WINDOW.mainloop()

main()