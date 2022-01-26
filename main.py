# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter.messagebox
from tkinter import Tk, Frame, Menu, Entry, RIGHT, Button, StringVar, Text
import json
from sympy import *
import screeninfo
from platform import system
import customtkinter

# TODO font calculation for different resolution macbook 20, hp 16
APP_NAME = "Scientific Calculator"
CONFIRM_MESSAGE = "Are you sure you want to exit?"
FONT_TUPLE = ("Arial", 16, "bold")

config_file = open("build.json")
config = json.load(config_file)

x = symbols("x")
init_printing()
Integral(sqrt(1 / x), x)

for monitor in screeninfo.get_monitors():
    print(monitor.width)
    print(monitor.height)

height = 500
if system() in ("Linux", "Windows"):
    height = 550

customtkinter.set_appearance_mode("Dark")
customtkinter.disable_macos_darkmode()
customtkinter.customtkinter_color_manager.CTkColorManager().set_main_color(None, None)
root = customtkinter.CTk()

root.title(APP_NAME)
# root.configure(background="Powder blue")
root.resizable(width=False, height=False)
root.geometry("358x" + str(height) + "+300+300")

calc = customtkinter.CTkFrame(master=root, corner_radius=0, fg_color="#000000")
calc.grid()


def is_okay(why, where, what):
    valid_inputs = ("^", "/", "(", ")", "%", "!", ".", "-", "+", "*")

    entryVar.set(entryVar.get() + what)
    print(entryVar.get())
    return what.isnumeric() or what in valid_inputs


txt_display = customtkinter.CTkEntry(calc, font=("Arial", 55), corner_radius=0, fg_color="#000000", height=120,
                                     width=358, validate="key")
txt_display.grid(row=0, column=0, columnspan=4, sticky="we")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

entryVar = StringVar()
ok_command = txt_display.register(is_okay)
txt_display.configure(validatecommand=(ok_command, "%d", "%i", "%S"))

buttons = []
for (row_index, buttons_row) in enumerate(config["buttons"]):
    buttons.append([])
    for (index, btn) in enumerate(buttons_row):
        size = 76 - (len(btn["txt"]) * 16)
        if size < 0:
            size = 76
        buttons[row_index].append(
            customtkinter.CTkButton(master=calc, width=76, height=76, corner_radius=38, text_font=FONT_TUPLE,
                                    fg_color=btn["bg"], text=""))
        if btn["colspan"] > 1:
            buttons[row_index][index].grid(row=row_index + 1, columnspan=btn["colspan"], padx=5, pady=5,
                                           column=btn["col"], sticky="we")
        else:
            buttons[row_index][index].grid(row=row_index + 1, padx=5, pady=5, column=btn["col"])
        label = customtkinter.CTkLabel(master=buttons[row_index][index],
                                       text=btn["txt"],
                                       fg_color=btn["bg"],
                                       width=30,
                                       text_font=FONT_TUPLE,
                                       corner_radius=0)
        label.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)


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
    root.geometry("1125x" + str(height) + "+300+300")
    txt_display.grid_configure(columnspan=13)


def calc_standard():
    root.geometry("358x" + str(height) + "+300+300")
    txt_display.grid_configure(columnspan=13)


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
