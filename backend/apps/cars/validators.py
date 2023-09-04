import re

from rest_framework.exceptions import ValidationError


class CarValidator:
    msg_bad_words = 'This content has some bad words!!!'
    bad_words = ['fuck', 'dick', 'shit', 'bitch']

    @staticmethod
    def validate_content(value):
        for word in CarValidator.bad_words:
            if re.search(rf'\b{re.escape(word)}\b', value, re.IGNORECASE):
                raise ValidationError(CarValidator.msg_bad_words)


