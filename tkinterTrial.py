import tkinter

labelText = "Welcome"

windowObj = tkinter.Tk()
windowObj.title("Welcome!")
labelObj = tkinter.Label(windowObj, text=labelText)
labelObj.pack()
windowObj.mainloop()

