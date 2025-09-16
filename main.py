import tkinter

# image location
IMGPATH = './img/frog.png'

# initialize window
WINDOW = tkinter.Tk()
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0
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
START_POSITION_X = 0
START_POSITION_Y = 0

# Image initilization
IMG = None

# Start the program by setting all the values to what they should be
def wake_up():
    global IMG, WINDOW_WIDTH, WINDOW_HEIGHT, START_POSITION_X, START_POSITION_Y

    # set the image
    IMG = tkinter.PhotoImage(file=IMGPATH)

    # Set the width and height
    WINDOW_WIDTH = IMG.width()
    WINDOW_HEIGHT = IMG.height()

    # Set the start position
    START_POSITION_X = SCREEN_WIDTH - WINDOW_WIDTH - 50
    START_POSITION_Y = SCREEN_HEIGHT - WINDOW_HEIGHT - 50

    # make a label
    label = tkinter.Label(image=IMG, bd=0)
    label.pack()

    # Set the location
    WINDOW.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{START_POSITION_X}+{START_POSITION_Y}')


def main():
    wake_up()

    # main loop
    WINDOW.mainloop()

if __name__ == "__main__":
    main()