from django.core.exceptions import ValidationError
import re

class UppercaseValidator:

    def validate(self, password, user=None):
        if not re.search(r'[A-ZĄČĘĖĮŠŲŪŽ]', password):
            raise ValidationError(
                "Slaptažodyje turi būti bent viena didžioji raidė.",
                code="password_no_upper",
            )

    def get_help_text(self):
        return "Slaptažodyje turi būti bent viena didžioji raidė."


class NumberValidator:

    def validate(self, password, user=None):
        if not re.search(r'\d', password):
            raise ValidationError(
                "Slaptažodyje turi būti bent vienas skaičius.",
                code="password_no_number",
            )

    def get_help_text(self):
        return "Slaptažodyje turi būti bent vienas skaičius."
