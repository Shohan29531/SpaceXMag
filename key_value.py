import keyboard



while(1):

    if keyboard.is_pressed('ctrl') and keyboard.is_pressed('s'):
        print("pressed")
    if(keyboard.is_pressed('e')):
        break 
    print("nope")   


# from tkinter import *

# def doSomething(event):
#     #print("You pressed: " + event.keysym)
#     label.config(text=event.keysym)

# window = Tk()

# window.bind("<Key>",doSomething)

# label = Label(window,font=("Helvetica",100))
# label.pack()

# window.mainloop()