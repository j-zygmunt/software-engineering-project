import tkinter
import assets
from abc import ABC, abstractmethod


class MainFrame(tkinter.Frame):

    def __init__(self, master, controller):
        super().__init__(master)
        self.__controller = controller
        self.__master = master
        self.__entry = None
        self.__remaining_attempts_counter = None
        self.__check_button = None
        self.__popup = None
        self.__entry_var = tkinter.StringVar()
        assets.Assets.load()
        self.__set_window_properties()
        self.start_window_layout()

    def __set_window_properties(self):
        self.__master.geometry("412x520")
        self.__master.resizable(0, 0)
        self.__master.title("Mastermind")

    def start_window_layout(self):
        self.__set_background()

        play_button = tkinter.Button(self, command=self.__controller.restart_button_action,
                                     image=assets.Assets.PLAY_BUTTON)
        play_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def game_window_layout(self):
        self.__set_background()

        self.__remaining_attempts_counter = tkinter.Label(self, font='Calibri 13 bold', bg='grey')
        self.__remaining_attempts_counter.config(width=2, borderwidth=2, relief="ridge", text="12")
        self.__remaining_attempts_counter.place(relx=0.05, rely=0.05)

        guesses_label = tkinter.Label(self, image=assets.Assets.YOUR_GUESS)
        guesses_label.place(relx=0.3, rely=0.15, anchor=tkinter.CENTER)

        answers_label = tkinter.Label(self, image=assets.Assets.ANSWERS)
        answers_label.place(relx=0.7, rely=0.15, anchor=tkinter.CENTER)

        guess_frame = tkinter.Frame(self, height=10, width=15, bg='#707271')
        self.__entry = tkinter.Entry(guess_frame, textvariable=self.__entry_var)
        self.__entry.config(width=7, font="Calibri 13 bold", justify='center')
        self.__entry.grid(row=0, column=1)
        here_label = tkinter.Label(guess_frame, image=assets.Assets.GUESS, bg='#707271')
        here_label.grid(row=0, column=0)
        guess_frame.place(relx=0.5, rely=0.98, anchor=tkinter.S)

        self.__check_button = tkinter.Button(self, command=self.__controller.check_button_action,
                                             image=assets.Assets.CHECK_BUTTON)
        self.__check_button.place(relx=0.85, rely=0.98, anchor=tkinter.S)

        restart_button = tkinter.Button(self, command=self.__controller.restart_button_action,
                                        image=assets.Assets.RESTART_BUTTON_WINDOW)
        restart_button.place(relx=0.15, rely=0.98, anchor=tkinter.S)

        back_button = tkinter.Button(self, command=self.__controller.back_button_action,
                                     image=assets.Assets.BACK_BUTTON)
        back_button.place(relx=0.98, rely=0.02, anchor=tkinter.NE)

    def __set_background(self):
        if self.__popup is not None:
            self.__popup.destroy()
        self.__entry_var.set("")
        objects = self.place_slaves()
        for obj in objects:
            obj.destroy()

        self.place(x=0, y=0, anchor="nw", width=412, height=520)
        window_background_label = tkinter.Label(self)
        window_background_label.config(image=assets.Assets.WINDOW_BACKGROUND)
        window_background_label.place(relwidth=1, relheight=1)

    def show_error_popup(self, message: str):
        self.__popup = ErrorPopup(self, message)
        self.__entry_var.set("")

    def show_endgame_popup(self, message: str):
        self.__entry.config(state='disabled')
        self.__check_button.config(state='disabled')
        self.__popup = EndGamePopup(self, message)

    def get_cords(self):
        return self.__master.winfo_x() + self.__master.winfo_width() / 2, \
               self.__master.winfo_y() + self.__master.winfo_height() / 2

    def update_view(self, iteration: int, remaining: int, output: tuple):
        self.__remaining_attempts_counter.config(text=str(remaining))

        guess_frame = tkinter.Frame(self, bg='grey')
        answer_frame = tkinter.Frame(self, bg='grey')

        guess_label = tkinter.Label(guess_frame, text=self.__entry_var.get())
        guess_label.config(font='Calibri 12 bold', background='grey')
        guess_label.grid(row=0, column=0, padx=10, pady=0)

        for i in range(output[0]):
            canvas = tkinter.Canvas(answer_frame, width=7, height=7, bg='black', bd=0)
            canvas.grid(row=0, column=i + 1, padx=4, pady=4)

        for i in range(output[1]):
            canvas = tkinter.Canvas(answer_frame, width=7, height=7, bg='white', bd=0)
            canvas.grid(row=0, column=i + 1 + output[0], padx=4, pady=4)

        guess_frame.place(relx=0.3, rely=0.17 + iteration * 0.055, anchor=tkinter.CENTER)
        answer_frame.place(relx=0.7, rely=0.17 + iteration * 0.055, anchor=tkinter.CENTER)

    def restart(self):
        self.__controller.restart_button_action()

    def get_entry_var(self):
        return self.__entry_var.get()


class PopupWindow(ABC, tkinter.Toplevel):

    @abstractmethod
    def __init__(self, parent, text: str):
        super().__init__(parent)
        self._parent = parent
        self._close_button = None
        self._text = text
        self.__set_window_layout()
        self._set_window_components()

    def __set_window_layout(self):
        self.config(bg='#707271')
        self.grab_set()
        self.focus_force()
        x, y = self._parent.get_cords()
        self.maxsize(200, 80)
        self.minsize(200, 80)
        self.geometry("+%d+%d" % (x - 100, y - 40))
        self.resizable(0, 0)

    @abstractmethod
    def _set_window_components(self):
        pass


class ErrorPopup(PopupWindow):

    def __init__(self, parent, text: str):
        super().__init__(parent, text)

    def _set_window_components(self):
        self.title("Error")
        label = tkinter.Label(self, text=self._text, bg='#707271')
        label.pack(pady=10)
        self._close_button = tkinter.Button(self, command=self.destroy, image=assets.Assets.CLOSE_BUTTON)
        self._close_button.place(x=72.5, y=45)


class EndGamePopup(PopupWindow):

    def __init__(self, parent, text: str):
        super().__init__(parent, text)
        self.__restart_button = None

    def _set_window_components(self):
        self.title("")
        label = tkinter.Label(self, text=self._text, bg='#707271')
        label.pack(pady=10)
        self._close_button = tkinter.Button(self, command=self.destroy, image=assets.Assets.CLOSE_BUTTON)
        self._close_button.place(x=8.75, y=45)
        self.__restart_button = tkinter.Button(self, command=self._parent.restart,
                                               image=assets.Assets.RESTART_BUTTON_END)
        self.__restart_button.place(x=136.25, y=45)
