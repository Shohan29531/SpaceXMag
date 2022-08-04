# import keyboard



# while(1):

#     if keyboard.is_pressed('ctrl') and keyboard.is_pressed('s'):
#         print("pressed")
#     if(keyboard.is_pressed('e')):
#         break 
#     print("nope")   


# from tkinter import *

# def doSomething(event):
#     #print("You pressed: " + event.keysym)
#     label.config(text=event.keysym)

# window = Tk()

# window.bind("<Key>",doSomething)

# label = Label(window,font=("Helvetica",100))
# label.pack()

# window.mainloop()


from pynput import keyboard

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()