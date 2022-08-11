from tkinter import Tk, Canvas
from PIL import ImageTk, Image

def main():
    root = Tk()

    canvas = Canvas(root, width=1080, height=1920)
    canvas.pack(fill="both", expand=True)

    im = Image.open('100*100.png')

    canvas.image = ImageTk.PhotoImage(im)

    canvas.create_image(0, 0, image=canvas.image, anchor='nw')

    canvas.bind("<ButtonPress-1>", drag_start)
    canvas.bind("<B1-Motion>", drag_move)

    root.mainloop()


def drag_start(event):
    event.widget.scan_mark(event.x, event.y)

def drag_move(event):
    event.widget.scan_dragto(event.x, event.y, gain=1)

if __name__ == "__main__":
    main()