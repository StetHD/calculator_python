import tkinter as tk
from tkinter import ttk
import sympy as sp
from io import BytesIO
from PIL import Image, ImageTk


def integrate():
    y = sp.symbols('y')
    r = sp.sqrt(y)
    x = sp.Symbol('x')
    integral = sp.integrate(eq.get(), x)
    var.set('Integration result=' + 'C\u2081')
    obj = BytesIO()
    sp.preview(r, viewer='BytesIO', output='svg', outputbuffer=obj)
    obj.seek(0)
    img_lbl.img = ImageTk.PhotoImage(Image.open(obj))
    img_lbl.config(image=img_lbl.img)


win = tk.Tk()  # defines window

win2 = ttk.Labelframe(win, text='')
win2.grid(column=0, row=0)

# Creates a static txt label
eq_static = ttk.Label(win2, text='Introduce the equation f(x)', font=("Times New Roman", 14))
eq_static.grid(column=0, row=0, padx=5, pady=5)

eq = tk.StringVar(value='4*x')
eq_Entered = ttk.Entry(win2, width=40, textvariable=eq)
eq_Entered.grid(column=1, row=0, padx=5, pady=5)
# Creates a static txt label
var = tk.StringVar()
eq_static = ttk.Label(win2, textvariable=var, font=("Times New Roman", 14))
var.set('Result')
eq_static.grid(column=0, row=3, padx=5, pady=5)
# Calculate button

img_lbl = tk.Label(win2)
img_lbl.grid()

action = ttk.Button(win2, text='Integrate', command=integrate)
action.grid(column=2, row=0, padx=5, pady=5)
win2.mainloop()
