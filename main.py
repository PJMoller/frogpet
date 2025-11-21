import tkinter
import os
import random
from PIL import Image, ImageTk

# Paths
IMG_DIR = os.path.join(os.path.dirname(__file__), 'img')
IMGPATH_FROG_IDLE = os.path.join(IMG_DIR, 'frog.png')
IMGPATH_FROG_LEFT = os.path.join(IMG_DIR, 'frog-left.gif')
IMGPATH_FROG_RIGHT = os.path.join(IMG_DIR, 'frog-right.gif')
IMGPATH_BUBBLE = os.path.join(IMG_DIR, 'bubble.png')

# Initialize window
WINDOW = tkinter.Tk()
WINDOW.configure(bg='')
WINDOW.overrideredirect(True)
WINDOW.focus_force()
WINDOW.bind("<Escape>", lambda e: WINDOW.destroy())
WINDOW.wm_attributes("-topmost", True)

SCREEN_WIDTH = WINDOW.winfo_screenwidth()
SCREEN_HEIGHT = WINDOW.winfo_screenheight()

# State variables
CURRENT_POSITION_X = 0
CURRENT_POSITION_Y = 0
CURRENT_BEHAVIOR = "idle"  # idle, walk_left, walk_right, talk
SPEED = 3  # pixels per step

# Images
IMG_IDLE = None
FRAMES_LEFT = []
FRAMES_RIGHT = []
CURRENT_FRAME_INDEX = 0
LABEL = None

# Bubble
BUBBLE_IMG = None
BUBBLE_WINDOW = None

def load_gif_frames(path):
    """Extract all frames from a GIF."""
    frames = []
    try:
        with Image.open(path) as img:
            while True:
                frame = ImageTk.PhotoImage(img.copy().convert("RGBA"))
                frames.append(frame)
                img.seek(len(frames))  # next frame
    except EOFError:
        pass
    return frames

def wake_up():
    global IMG_IDLE, FRAMES_LEFT, FRAMES_RIGHT
    global CURRENT_POSITION_X, CURRENT_POSITION_Y, LABEL, WINDOW_WIDTH, WINDOW_HEIGHT

    # Load images
    if not os.path.exists(IMGPATH_FROG_IDLE):
        raise FileNotFoundError(IMGPATH_FROG_IDLE)
    if not os.path.exists(IMGPATH_FROG_LEFT):
        raise FileNotFoundError(IMGPATH_FROG_LEFT)
    if not os.path.exists(IMGPATH_FROG_RIGHT):
        raise FileNotFoundError(IMGPATH_FROG_RIGHT)

    IMG_IDLE = tkinter.PhotoImage(file=IMGPATH_FROG_IDLE)
    FRAMES_LEFT = load_gif_frames(IMGPATH_FROG_LEFT)
    FRAMES_RIGHT = load_gif_frames(IMGPATH_FROG_RIGHT)

    WINDOW_WIDTH = IMG_IDLE.width()
    WINDOW_HEIGHT = IMG_IDLE.height()

    CURRENT_POSITION_X = SCREEN_WIDTH - WINDOW_WIDTH - 50
    CURRENT_POSITION_Y = SCREEN_HEIGHT - WINDOW_HEIGHT - 50

    LABEL = tkinter.Label(image=IMG_IDLE, bg='white', bd=0)
    LABEL.pack()

    WINDOW.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{CURRENT_POSITION_X}+{CURRENT_POSITION_Y}')
    WINDOW.wm_attributes('-transparentcolor', 'white')

def chatbubble():
    global BUBBLE_IMG, BUBBLE_WINDOW

    if not os.path.exists(IMGPATH_BUBBLE):
        raise FileNotFoundError(IMGPATH_BUBBLE)

    BUBBLE_WINDOW = tkinter.Toplevel(WINDOW)
    BUBBLE_WINDOW.overrideredirect(True)
    BUBBLE_WINDOW.focus_force()
    BUBBLE_WINDOW.bind("<Escape>", lambda e: WINDOW.destroy())
    BUBBLE_WINDOW.wm_attributes("-topmost", True)

    pil_image = Image.open(IMGPATH_BUBBLE).convert("RGBA")
    BUBBLE_IMG = ImageTk.PhotoImage(pil_image)

    bubble_x = CURRENT_POSITION_X - 50
    bubble_y = CURRENT_POSITION_Y - BUBBLE_IMG.height() + 20

    label = tkinter.Label(BUBBLE_WINDOW, image=BUBBLE_IMG, bg='black', bd=0)
    label.pack()

    BUBBLE_WINDOW.geometry(f'{BUBBLE_IMG.width()}x{BUBBLE_IMG.height()}+{bubble_x}+{bubble_y}')
    BUBBLE_WINDOW.wm_attributes('-transparentcolor', 'black')

def update_bubble_visibility():
    """Show bubble only when frog is talking."""
    if BUBBLE_WINDOW:
        if CURRENT_BEHAVIOR == "talk":
            BUBBLE_WINDOW.deiconify()  # show bubble
        else:
            BUBBLE_WINDOW.withdraw()   # hide bubble
    WINDOW.after(200, update_bubble_visibility)

def change_behaviour():
    """Randomly switch between behaviors."""
    global CURRENT_BEHAVIOR
    CURRENT_BEHAVIOR = random.choice(["idle", "walk_left", "walk_right", "talk"])
    print(f"Now performing: {CURRENT_BEHAVIOR}")
    WINDOW.after(random.randint(3000, 6000), change_behaviour)

def animate_frog():
    """Display the next frame of the frog animation."""
    global CURRENT_FRAME_INDEX

    if CURRENT_BEHAVIOR == "walk_left":
        frames = FRAMES_LEFT
    elif CURRENT_BEHAVIOR == "walk_right":
        frames = FRAMES_RIGHT
    else:
        LABEL.configure(image=IMG_IDLE)
        WINDOW.after(150, animate_frog)
        return

    if not frames:
        return

    LABEL.configure(image=frames[CURRENT_FRAME_INDEX])
    CURRENT_FRAME_INDEX = (CURRENT_FRAME_INDEX + 1) % len(frames)

    WINDOW.after(120, animate_frog)

def move_frog():
    """Move the frog smoothly based on current behavior."""
    global CURRENT_POSITION_X

    if CURRENT_BEHAVIOR == "walk_left":
        CURRENT_POSITION_X = max(0, CURRENT_POSITION_X - SPEED)
    elif CURRENT_BEHAVIOR == "walk_right":
        CURRENT_POSITION_X = min(SCREEN_WIDTH - WINDOW_WIDTH, CURRENT_POSITION_X + SPEED)

    # Update bubble position if it exists
    if BUBBLE_IMG and BUBBLE_WINDOW:
        bubble_x = CURRENT_POSITION_X - 50
        bubble_y = CURRENT_POSITION_Y - BUBBLE_IMG.height() + 20
        BUBBLE_WINDOW.geometry(f'{BUBBLE_IMG.width()}x{BUBBLE_IMG.height()}+{bubble_x}+{bubble_y}')

    WINDOW.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{CURRENT_POSITION_X}+{CURRENT_POSITION_Y}')
    WINDOW.after(50, move_frog)

def main():
    try:
        wake_up()
        chatbubble()
        update_bubble_visibility()
        change_behaviour()
        move_frog()
        animate_frog()
        WINDOW.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
