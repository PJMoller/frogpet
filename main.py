import tkinter
import random

number = random.randint(10, 1000)

IMGPATH = './img/frog.png'
WINDOW = tkinter.Tk()
WINDOW.geometry('420x420+'+str(number)+'+100')

def main():
    # set the image
    img = tkinter.PhotoImage(file=IMGPATH)

    # make a label
    label = tkinter.Label(image=img, bd=0)
    label.pack()

    # main loop
    WINDOW.mainloop()

main()