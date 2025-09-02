import tkinter
import random

IMGPATH = './img/frog.png'
WINDOW = tkinter.Tk()

def main():
    # set the image
    img = tkinter.PhotoImage(file=IMGPATH)

    # make a label
    label = tkinter.Label(image=img)
    label.pack()

    # main loop
    WINDOW.mainloop()

main()