import copy
import random
import constants


class InappropriateCodeException(Exception):

    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self) -> str:
        return self.message


class CodeLogic:

    @staticmethod
    def check_code_validness(code: list):
        temp_code = copy.copy(code)
        try:
            temp_code = [int(pin) for pin in temp_code]
        except ValueError:
            raise InappropriateCodeException("Kod musi składać się z samych cyfr.")
        for pin in temp_code:
            if pin < 1 or pin > constants.NUMBER_OF_PINS:
                raise InappropriateCodeException("Dozwolone tylko cyfry od 1 do 6.")
        if len(temp_code) != constants.CODE_LENGTH:
            raise InappropriateCodeException("Kod musi mieć długość = 4.")

    @staticmethod
    def check_code(guess: list, code: list) -> tuple:
        black_dot = 0
        white_dot = 0
        temp_code = copy.copy(code)
        temp_guess = copy.copy(guess)
        for i in range(constants.CODE_LENGTH):
            if temp_guess[i] == code[i]:
                black_dot += 1
                temp_code.remove(guess[i])
                temp_guess[i] = None
        for i in range(constants.CODE_LENGTH):
            if temp_guess[i] in temp_code:
                white_dot += 1
                temp_code.remove(guess[i])
                temp_guess[i] = None
        return black_dot, white_dot

    @staticmethod
    def get_random_code() -> list:
        return [random.randint(1, constants.NUMBER_OF_PINS) for _ in range(constants.CODE_LENGTH)]


class Player:

    def __init__(self):
        self.__code = CodeLogic.get_random_code()
        self.__count_guesses = 0

    def get_code(self) -> list:
        return self.__code

    def set_code(self, code: list):
        self.__code = code

    def get_count_guesses(self) -> int:
        return self.__count_guesses

    def get_remaining_attempts(self) -> int:
        return constants.MAX_GUESSES - self.__count_guesses

    def increment_count_guesses(self):
        self.__count_guesses += 1

    def get_initial_state(self):
        self.__count_guesses = 0
        self.__code = CodeLogic.get_random_code()
