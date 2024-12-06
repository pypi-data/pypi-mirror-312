from typing import Union

from mastermind.players.abstract_player import CodeSetter
from mastermind.validation import (
    InputConversionError,
    RangeError,
    TypeValidationError,
    ValidFeedback,
)


class ExternalCodeSetter(CodeSetter):
    def set_secret_code(self) -> None:
        pass  # There is no code available for external game, skip it

    def get_feedback(self, guess: tuple) -> Union[tuple, str]:
        valid_feedback = ValidFeedback(number_of_dots=self.game_state.number_of_dots)
        while True:
            feedback = input("Enter the feedback: ")
            if feedback == "?":
                hint = f"""
                Enter a 2 digit number (optionally separated by comma) between 0 and {self.game_state.number_of_dots}.
                The first digit represents the number of black pegs, the second represents the number of white pegs.
                For example: 01 or 0,1 -> (0, 1) -> 0 black pegs, 1 white peg.
                Or, you can enter a command:
                (?) for help
                (d) to discard the game
                (q) to save and quit
                (u) to undo
                """
                print(hint)
                continue
            if feedback == "d":
                print("Game discarded.")
                return "d"
            if feedback == "q":  # quit
                print("Game saved.")
                return "q"
            if feedback == "u":  # undo
                return "u"

            try:
                valid_feedback.value = valid_feedback.validate_value(feedback)
                return valid_feedback.value
            except (TypeValidationError, InputConversionError) as e:
                print(e)
                print("To get more help, enter '?'")

            except RangeError:
                print(
                    f"Feedback must consist of 2 integer in range [0, {self.game_state.number_of_dots})"
                )
                print("To get more help, enter '?'")
