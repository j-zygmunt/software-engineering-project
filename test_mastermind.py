import unittest
import mastermind_model


class TestMastermind(unittest.TestCase):

    def test_completely_wrong_code(self):

        player = mastermind_model.Player()
        player.set_code([1, 1, 1, 1])
        black, white = mastermind_model.CodeLogic.check_code([2, 2, 2, 2], player.get_code())
        self.assertEqual(black, 0)
        self.assertEqual(white, 0)

        black, white = mastermind_model.CodeLogic.check_code([4, 5, 4, 5], player.get_code())
        self.assertEqual(black, 0)
        self.assertEqual(white, 0)

    def test_wrong_positions_human(self):

        player = mastermind_model.Player()
        player.set_code([6, 3, 6, 1])
        black, white = mastermind_model.CodeLogic.check_code([3, 6, 1, 6], player.get_code())
        self.assertEqual(black, 0)
        self.assertEqual(white, 4)

        black, white = mastermind_model.CodeLogic.check_code([1, 6, 3, 6], player.get_code())
        self.assertEqual(black, 0)
        self.assertEqual(white, 4)

        black, white = mastermind_model.CodeLogic.check_code([1, 1, 1, 3], player.get_code())
        self.assertEqual(black, 0)
        self.assertEqual(white, 2)

    def test_correct_digits_and_wrong_positions(self):

        player = mastermind_model.Player()
        player.set_code([1, 2, 3, 4])
        black, white = mastermind_model.CodeLogic.check_code([2, 1, 3, 4], player.get_code())
        self.assertEqual(black, 2)
        self.assertEqual(white, 2)

        black, white = mastermind_model.CodeLogic.check_code([4, 2, 3, 1], player.get_code())
        self.assertEqual(black, 2)
        self.assertEqual(white, 2)

        black, white = mastermind_model.CodeLogic.check_code([4, 4, 4, 4], player.get_code())
        self.assertEqual(black, 1)
        self.assertEqual(white, 0)

    def test_code_validness(self):

        player = mastermind_model.Player()

        'too long'
        invalid_input = '12345'

        with self.assertRaises(mastermind_model.InappropriateCodeException) as context:
            mastermind_model.CodeLogic.check_code_validness(invalid_input)

        self.assertTrue('Kod musi mieć długość = 4.' in str(context.exception))

        'too short'
        invalid_input = '123'

        with self.assertRaises(mastermind_model.InappropriateCodeException) as context:
            mastermind_model.CodeLogic.check_code_validness(invalid_input)

        self.assertTrue('Kod musi mieć długość = 4.' in str(context.exception))

        'not digits'
        invalid_input = 'asdas'

        with self.assertRaises(mastermind_model.InappropriateCodeException) as context:
            mastermind_model.CodeLogic.check_code_validness(invalid_input)

        self.assertTrue('Kod musi składać się z samych cyfr.' in str(context.exception))

        'special chars'
        invalid_input = ' $@_+'

        with self.assertRaises(mastermind_model.InappropriateCodeException) as context:
            mastermind_model.CodeLogic.check_code_validness(invalid_input)

        self.assertTrue('Kod musi składać się z samych cyfr.' in str(context.exception))

        'digit out of range'
        invalid_input = '1228'

        with self.assertRaises(mastermind_model.InappropriateCodeException) as context:
            mastermind_model.CodeLogic.check_code_validness(invalid_input)

        self.assertTrue('Dozwolone tylko cyfry od 1 do 6.' in str(context.exception))