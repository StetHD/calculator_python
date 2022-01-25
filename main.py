# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter.messagebox
from tkinter import Tk, Frame, Menu, Entry, RIGHT, Button, StringVar
import json
from sympy import *

APP_NAME = "Scientific Calculator"
CONFIRM_MESSAGE = "Are you sure you want to exit?"
FONT_TUPLE = ("Arial", 20, "bold")

config_file = open("buid.json")
config = json.load(config_file)

x = symbols("x")
init_printing()
Integral(sqrt(1/x), x)

root = Tk()
root.title(APP_NAME)
root.configure(background="Powder blue")
root.resizable(width=False, height=False)
root.geometry("358x500+300+300")

calc = Frame(root)
calc.grid()


def is_okay(why, where, what):
    valid_inputs = ("^", "/", "(", ")", "%", "!", ".", "-", "+", "*")

    entryVar.set(entryVar.get() + what)
    print(entryVar.get())
    return what.isnumeric() or what in valid_inputs


txt_display = Entry(calc, font=FONT_TUPLE, bg="powder blue", bd=30, width=29, borderwidth=1, justify=RIGHT,
                    insertofftime=0, validate="key")
txt_display.grid(row=0, column=0, columnspan=4, pady=1, sticky="we", ipady="30")
entryVar = StringVar()
ok_command = txt_display.register(is_okay)
txt_display.configure(validatecommand=(ok_command, "%d", "%i", "%S"))

buttons = []
for (row_index, buttons_row) in enumerate(config["buttons"]):
    buttons.append([])
    for (index, btn) in enumerate(buttons_row):
        buttons[row_index].append(Button(calc, width=3, height=3, font=FONT_TUPLE, bd=2, text=btn["txt"], bg="#000000"))
        buttons[row_index][index].grid(row=row_index + 1, columnspan=btn["colspan"], column=btn["col"], sticky="we")

# clear_button = Button(calc, width=3, height=3, font=FONT_TUPLE, bd=2, bg="Powder blue", text=chr(67))
# clear_button.grid(row=1, column=0, pady=1)
#
#
# clear_all_button = Button(calc, width=3, height=3, font=FONT_TUPLE, bd=2, bg="Powder blue", text=chr(67) + chr(69))
# clear_all_button.grid(row=1, column=1, pady=1)


# ===============MENU===================

def calc_exit():
    app_exit = tkinter.messagebox.askyesno(APP_NAME, CONFIRM_MESSAGE)
    if app_exit > 0:
        root.destroy()
        return


def calc_scientific():
    root.resizable(width=False, height=False)
    root.geometry("935x500+300+300")
    txt_display.grid(row=0, column=0, columnspan=13, pady=1, sticky="we", ipady="30")
    txt_display.update()


def calc_standard():
    root.resizable(width=False, height=False)
    root.geometry("358x500+300+300")
    txt_display.grid(row=0, column=0, columnspan=4, pady=1, sticky="we", ipady="30")
    txt_display.update()


menubar = Menu(calc)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Standard", command=calc_standard)
file_menu.add_command(label="Scientific", command=calc_scientific)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=calc_exit)

edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_separator()
edit_menu.add_command(label="Paste")

help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="View Help")

root.configure(menu=menubar)
root.mainloop()

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
