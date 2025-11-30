import tkinter
import os
import random
from PIL import Image, ImageTk, ImageDraw, ImageFont

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

# Images and animation
IMG_IDLE = None
FRAMES_LEFT = []
FRAMES_RIGHT = []
CURRENT_FRAME_INDEX = 0
LABEL = None

# Bubble
BUBBLE_BASE = None
BUBBLE_IMG = None
BUBBLE_LABEL = None
BUBBLE_WINDOW = None

# Store last displayed text (prevents flashing)
LAST_BUBBLE_TEXT = ""


def load_gif_frames(path):
    """Extract all frames from a GIF."""
    frames = []
    try:
        with Image.open(path) as img:
            while True:
                frame = ImageTk.PhotoImage(img.copy().convert("RGBA"))
                frames.append(frame)
                img.seek(len(frames))
    except EOFError:
        pass
    return frames


def wake_up():
    global IMG_IDLE, FRAMES_LEFT, FRAMES_RIGHT
    global CURRENT_POSITION_X, CURRENT_POSITION_Y, LABEL
    global WINDOW_WIDTH, WINDOW_HEIGHT

    # Load images
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
    """Creates the bubble window and stores a clean base image."""
    global BUBBLE_WINDOW, BUBBLE_LABEL, BUBBLE_IMG, BUBBLE_BASE

    BUBBLE_WINDOW = tkinter.Toplevel(WINDOW)
    BUBBLE_WINDOW.overrideredirect(True)
    BUBBLE_WINDOW.focus_force()
    BUBBLE_WINDOW.bind("<Escape>", lambda e: WINDOW.destroy())
    BUBBLE_WINDOW.wm_attributes("-topmost", True)

    # Load base bubble image (unmodified)
    BUBBLE_BASE = Image.open(IMGPATH_BUBBLE).convert("RGBA")

    # Create initial bubble image
    BUBBLE_IMG = ImageTk.PhotoImage(BUBBLE_BASE.copy())
    BUBBLE_LABEL = tkinter.Label(BUBBLE_WINDOW, image=BUBBLE_IMG, bg='black', bd=0)
    BUBBLE_LABEL.pack()

    # Position bubble initially
    bubble_x = CURRENT_POSITION_X - 50
    bubble_y = CURRENT_POSITION_Y - BUBBLE_BASE.height + 20
    BUBBLE_WINDOW.geometry(f'{BUBBLE_BASE.width}x{BUBBLE_BASE.height}+{bubble_x}+{bubble_y}')
    BUBBLE_WINDOW.wm_attributes('-transparentcolor', 'black')


def set_bubble_text(text: str):
    global BUBBLE_IMG, LAST_BUBBLE_TEXT

    # Avoid repeated redraw
    if text == LAST_BUBBLE_TEXT:
        return

    LAST_BUBBLE_TEXT = text

    img = BUBBLE_BASE.copy()
    draw = ImageDraw.Draw(img)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    # Get text bounding box (works in new Pillow versions)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Center inside bubble
    center_x = (img.width - text_w) // 2
    center_y = (img.height - text_h) // 2

    draw.text((center_x, center_y - 5), text, font=font, fill=(0, 0, 0, 255))

    BUBBLE_IMG = ImageTk.PhotoImage(img)
    BUBBLE_LABEL.configure(image=BUBBLE_IMG)


def update_bubble_visibility():
    """Shows bubble when talking, hides otherwise, and gives one text per talk."""
    global LAST_BUBBLE_TEXT

    if not BUBBLE_WINDOW:
        WINDOW.after(200, update_bubble_visibility)
        return

    if CURRENT_BEHAVIOR == "talk":
        # Show bubble
        BUBBLE_WINDOW.deiconify()

        # Only set text once per talk
        if LAST_BUBBLE_TEXT == "":
            line = random.choice([
                "Hello!",
                "Ribbit!",
                "What's up?",
                "Nice day!",
                "I'm a frog!",
                "Boing!"
            ])
            set_bubble_text(line)

    else:
        # Reset text and hide bubble
        LAST_BUBBLE_TEXT = ""
        BUBBLE_WINDOW.withdraw()

    WINDOW.after(200, update_bubble_visibility)


def change_behaviour():
    """Periodically pick a new action."""
    global CURRENT_BEHAVIOR
    CURRENT_BEHAVIOR = random.choice(["idle", "walk_left", "walk_right", "talk"])
    print(f"Now performing: {CURRENT_BEHAVIOR}")
    WINDOW.after(random.randint(3000, 6000), change_behaviour)


def animate_frog():
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
    """Smoothly move the frog across the screen."""
    global CURRENT_POSITION_X

    if CURRENT_BEHAVIOR == "walk_left":
        CURRENT_POSITION_X = max(0, CURRENT_POSITION_X - SPEED)
    elif CURRENT_BEHAVIOR == "walk_right":
        CURRENT_POSITION_X = min(SCREEN_WIDTH - WINDOW_WIDTH, CURRENT_POSITION_X + SPEED)

    # Move bubble with frog
    if BUBBLE_WINDOW:
        bubble_x = CURRENT_POSITION_X - 50
        bubble_y = CURRENT_POSITION_Y - BUBBLE_BASE.height + 20
        BUBBLE_WINDOW.geometry(f'{BUBBLE_BASE.width}x{BUBBLE_BASE.height}+{bubble_x}+{bubble_y}')

    # Move frog window
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
        print(f"Error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
