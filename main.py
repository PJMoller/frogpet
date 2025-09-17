import tkinter
from os import path
from PIL import Image, ImageTk  

# image location
IMGPATH_FROG = './img/frog.png'
IMGPATH_BUBBLE = './img/bubble.png'

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

# Keep track of current location
CURRENT_POSITION_X = 0
CURRENT_POSITION_Y = 0

# Image initilization
IMG = None
BUBBLE_IMG = None
BUBBLE_WINDOW = None

# Start the program by setting all the values to what they should be
def wake_up():
    global IMG, WINDOW_WIDTH, WINDOW_HEIGHT, START_POSITION_X, START_POSITION_Y, CURRENT_POSITION_X, CURRENT_POSITION_Y

    if not path.exists(IMGPATH_FROG):
        raise FileNotFoundError(f"Image file not found: {IMGPATH_FROG}")

    IMG = tkinter.PhotoImage(file=IMGPATH_FROG)

    # Set the width and height
    WINDOW_WIDTH = IMG.width()
    WINDOW_HEIGHT = IMG.height()

    # Set the start position
    START_POSITION_X = SCREEN_WIDTH - WINDOW_WIDTH - 50
    START_POSITION_Y = SCREEN_HEIGHT - WINDOW_HEIGHT - 50

    # make a label
    label = tkinter.Label(image=IMG, bd=0)
    label.pack()

    CURRENT_POSITION_X = START_POSITION_X
    CURRENT_POSITION_Y = START_POSITION_Y

    # Set the location
    WINDOW.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{START_POSITION_X}+{START_POSITION_Y}')


def chatbubble():
    global BUBBLE_IMG, BUBBLE_WINDOW

    if not path.exists(IMGPATH_BUBBLE):
        raise FileNotFoundError(f"Image file not found: {IMGPATH_BUBBLE}")

    # Create a second window
    BUBBLE_WINDOW = tkinter.Toplevel(WINDOW)
    BUBBLE_WINDOW.overrideredirect(True)
    BUBBLE_WINDOW.focus_force()
    BUBBLE_WINDOW.bind("<Escape>", lambda e: WINDOW.destroy())

    # Make it so the background is transparent
    pil_image = Image.open(IMGPATH_BUBBLE).convert("RGBA")
    BUBBLE_IMG = ImageTk.PhotoImage(pil_image)

    # Position on bases on frog location
    bubble_x = CURRENT_POSITION_X - 130
    bubble_y = CURRENT_POSITION_Y - BUBBLE_IMG.height() + 20

    # Set label
    label = tkinter.Label(BUBBLE_WINDOW, image=BUBBLE_IMG, bg='black', bd=0) 
    label.pack()

    # Place window
    BUBBLE_WINDOW.geometry(f'{BUBBLE_IMG.width()}x{BUBBLE_IMG.height()}+{bubble_x}+{bubble_y}')

    # Make black transparent
    BUBBLE_WINDOW.wm_attributes('-transparentcolor', 'black')

def change_behaviour():
    return

def main(): 
    wake_up()
    chatbubble()
    change_behaviour()

    # main loop
    WINDOW.mainloop()

if __name__ == "__main__":
    main()