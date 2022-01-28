import customtkinter
from tkinter import Menu, messagebox, CENTER, StringVar, Label, RIGHT

from config_loader import Config
from helpers import geometry_string
from calc_core import Calculator

_config = Config("build.json")
_core = Calculator()


class CalculatorUi:
    def __init__(self, config=_config, calc_core=_core):
        self.__config = config
        self.__core = calc_core
        customtkinter.set_appearance_mode("Dark")
        customtkinter.disable_macos_darkmode()
        customtkinter.customtkinter_color_manager.CTkColorManager().set_main_color(None, None)
        self.__root = customtkinter.CTk()
        self.__root.title(config.app_name)
        self.__root.resizable(width=False, height=False)
        self.__root.geometry(geometry_string(config.window["min_width"], config.window["height"]))
        self.__main_frame = customtkinter.CTkFrame(master=self.__root, corner_radius=0, fg_color="#000000")
        self.__main_frame.grid()
        self.__input_var = StringVar(value=calc_core.result)
        self.__input_var.set("0")
        self.__input = customtkinter.CTkEntry(self.__main_frame, height=120, width=358, textvariable=self.__input_var,
                                              justify=RIGHT)
        self.__clr_btn = dict()

    def __calc_exit(self):
        app_exit = messagebox.askyesno(self.__config.app_name, self.__config.messages["confirm"])
        if app_exit > 0:
            self.__root.destroy()
            return

    def __calc_scientific(self):
        self.__root.geometry(geometry_string(self.__config.window["max_width"], self.__config.window["height"]))
        self.__input.grid_configure(columnspan=13)

    def __calc_standard(self):
        self.__root.geometry(geometry_string(self.__config.window["min_width"], self.__config.window["height"]))
        self.__input.grid_configure(columnspan=13)

    def __input_validation(self, calc_input):
        valid_inputs = ("^", "/", "(", ")", "%", "!", ".", "-", "+", "*")
        self.__core.insert(calc_input)
        return calc_input.isnumeric() or calc_input in valid_inputs

    def __create_menu(self):
        menubar = Menu(self.__main_frame)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Standard", command=self.__calc_standard)
        file_menu.add_command(label="Scientific", command=self.__calc_scientific)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.__calc_exit)

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_separator()
        edit_menu.add_command(label="Paste")

        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="View Help")

        self.__root.configure(menu=menubar)

    def __create_input(self):
        font = (self.__config.font["family"], 55)
        self.__input.configure(font=font, corner_radius=0, fg_color="#000000", text_color="#ffffff")
        self.__input.grid(row=0, column=0, columnspan=4, sticky="we")
        validation = self.__input.register(self.__input_validation)
        self.__input.configure(validatecommand=(validation, "%S"))

    def __update(self, value):
        self.__core.insert(value)
        self.__input_var.set("0" if self.__core.result == "" else self.__core.result)

        if self.__core.result != "":
            self.__clr_btn["label"].config(text="C")
            self.__clr_btn["label"].unbind_all("<Button-1>")
            self.__clr_btn["label"].bind("<Button-1>", lambda _, x="C": self.__update(x))

            self.__clr_btn["button"].configure(command=lambda x="C": self.__update(x))

        if self.__core.result == "":
            self.__clr_btn["label"].config(text="AC")
            self.__clr_btn["label"].unbind_all("<Button-1>")
            self.__clr_btn["label"].bind("<Button-1>", lambda _, x="AC": self.__update(x))

            self.__clr_btn["button"].configure(command=lambda x="AC": self.__update(x))

    def __create_buttons(self):
        font_big = (self.__config.font["family"], self.__config.font["big"]["size"],
                    self.__config.font["big"]["weight"])

        font_medium = (self.__config.font["family"], self.__config.font["medium"]["size"],
                       self.__config.font["medium"]["weight"])

        font_small = (self.__config.font["family"], self.__config.font["small"]["size"],
                      self.__config.font["small"]["weight"])

        buttons = []
        for (row_index, buttons_row) in enumerate(self.__config.buttons):
            buttons.append([])
            for (index, btn) in enumerate(buttons_row):
                button = customtkinter.CTkButton(master=self.__main_frame, width=76, height=76, corner_radius=38,
                                                 fg_color=btn["bg"], text="")
                button.grid(row=row_index + 1, padx=5, pady=5, column=btn["col"])
                if btn["colspan"] > 1:
                    button.grid_configure(columnspan=btn["colspan"], sticky="we")

                button.configure(command=lambda x=btn["cmd"]: self.__update(x))

                if btn["txt"] == "AC":
                    self.__clr_btn["button"] = button

                buttons[row_index].append(button)

                font = font_small if len(btn["txt"]) > 5 else font_medium if len(btn["txt"]) > 3 else font_big

                label = Label(master=buttons[row_index][index],
                              text=btn["txt"],
                              font=font,
                              bg=btn["bg"],
                              fg="#ffffff")
                label.bind("<Button-1>", lambda _, x=btn["cmd"]: self.__update(x))

                label.place(anchor=CENTER, relx=0.5, rely=0.5)
                if btn["txt"] == "AC":
                    self.__clr_btn["label"] = label

    def draw(self):
        self.__create_menu()
        self.__create_input()
        self.__create_buttons()
        self.__root.mainloop()
