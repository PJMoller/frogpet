import tkinter
import random

# image location
IMGPATH = './img/frog.png'

# initialize window
WINDOW = tkinter.Tk()

# make it so theres no background
WINDOW.configure(bg='')

# removes the program header
WINDOW.overrideredirect(True)

# make it so you can exit the program using the escape key
WINDOW.focus_force()
WINDOW.bind("<Escape>", lambda e: WINDOW.destroy())

def move_around():
    # set random x and y values
    x = random.randint(10, 1000)
    y = random.randint(10, 1000)

    # change the location of the window
    WINDOW.geometry(f'226x223+{x}+{y}')

    # call the function again after 50ms
    WINDOW.after(50, move_around)

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