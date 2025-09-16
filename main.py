import tkinter

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
START_POSITION_X = SCREEN_WIDTH - WINDOW_WIDTH - 50
START_POSITION_Y = SCREEN_HEIGHT - WINDOW_HEIGHT - 50
ACCELERATION_SPEED_X = 3
ACCELERATION_SPEED_Y = 3

IMG = None


def wake_up():
    global IMG

    # set the image
    IMG = tkinter.PhotoImage(file=IMGPATH)

    # make a label
    label = tkinter.Label(image=IMG, bd=0)
    label.pack()

def move_around():
    global START_POSITION_X, START_POSITION_Y, ACCELERATION_SPEED_X, ACCELERATION_SPEED_Y

    # update position
    START_POSITION_X += ACCELERATION_SPEED_X
    START_POSITION_Y += ACCELERATION_SPEED_Y

    if START_POSITION_X <= 0 or START_POSITION_X + WINDOW_WIDTH >= SCREEN_WIDTH:
        ACCELERATION_SPEED_X = -ACCELERATION_SPEED_X
    if START_POSITION_Y <= 0 or START_POSITION_Y + WINDOW_HEIGHT >= SCREEN_HEIGHT:
        ACCELERATION_SPEED_Y = -ACCELERATION_SPEED_Y

    WINDOW.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{START_POSITION_X}+{START_POSITION_Y}')

    # call the function again after 50ms
    WINDOW.after(50, move_around)

def main():
    wake_up()
    move_around()

    # main loop
    WINDOW.mainloop()

if __name__ == "__main__":
    main()