from tkinter import Tk, Canvas
from PIL import ImageTk, Image


canvas = None

def main():
    root = Tk()
    global canvas

    canvas = Canvas(root, width = 180, height = 240)
    canvas.pack(fill="both", expand=True)

    im = Image.open('test_image.png')

    canvas.image = ImageTk.PhotoImage(im)

    canvas.create_image(0, 0, image=canvas.image, anchor='center')

    canvas.bind("<ButtonPress-1>", zoom_in)
    canvas.bind("<ButtonPress-3>", zoom_out)
    canvas.bind("<Motion>", drag_move)

    root.mainloop()


def zoom_in(event):
    print("zoom in")
    event.widget.scale("all", event.x, event.y, 2, 2)

def zoom_out(event):
    print("zoom out")
    event.widget.scale("all", event.x, event.y, 0.5, 0.5)

def drag_start(event):
    event.widget.scan_mark(event.x, event.y)

def drag_move(event):
    event.widget.scan_dragto(event.x, event.y, gain=1)

if __name__ == "__main__":
    main()

 