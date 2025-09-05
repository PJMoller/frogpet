import tkinter
import random


IMGPATH = './img/frog.png'
WINDOW = tkinter.Tk()
WINDOW.configure(bg='')
WINDOW.overrideredirect(True)
WINDOW.focus_force()
WINDOW.bind("<Escape>", lambda e: WINDOW.destroy())

def move_around():
    x = random.randint(10, 1000)
    y = random.randint(10, 1000)
    WINDOW.geometry(f'226x223+{x}+{y}')
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