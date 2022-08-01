import tkinter as tk
from PIL import Image, ImageTk
import custom_fisheye_effect

IMG1 = "output_1.jpg"
IMG2 = "output_2.jpg"

class ExampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=540, height=960, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)

        self.image = Image.open(IMG1).resize((540, 960))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image((0, 0), anchor="nw", image=self.photo)
        self.bind('<Button-1>', self.update)

    def update(self, event):
        self.image = Image.open(IMG2).resize((540, 960))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image((0, 0), anchor="nw", image=self.photo)

if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()



apply_fisheye_effect(img_file = 'Output.jpg', fisheye_focus = (540, 960), fisheye_radius = 200 )