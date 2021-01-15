import mastermind_model
import mastermind_view
import tkinter


class Controller:

    def __init__(self, parent):
        self.__player = mastermind_model.Player()
        self.__view = mastermind_view.MainFrame(parent, self)

    def check_button_action(self):
        try:
            entry_var = self.__view.get_entry_var()
            mastermind_model.CodeLogic.check_code_validness(entry_var)
        except mastermind_model.InappropriateCodeException as error:
            self.__view.show_error_popup(error.__str__())
            return
        self.__player.increment_count_guesses()
        guess_number = self.__player.get_count_guesses()
        remaining = self.__player.get_remaining_attempts()
        output = mastermind_model.CodeLogic.check_code(entry_var, self.__player.get_code())
        self.__view.update_view(guess_number, remaining, output)
        if output[0] == 4 or remaining == 0:
            if output[0] == 4:
                text = 'Congratulations\nYou have won in ' + str(guess_number) + 'th attempt'
            else:
                text = 'Not this time\nThe code was: ' + ''.join([str(digit) for digit in self.__player.get_code()])
            self.__view.show_endgame_popup(text)

    def restart_button_action(self):
        self.__player.get_initial_state()
        self.__view.game_window_layout()

    def back_button_action(self):
        self.__player.get_initial_state()
        self.__view.start_window_layout()


if __name__ == "__main__":
    root = tkinter.Tk()
    controller = Controller(root)
    root.mainloop()
