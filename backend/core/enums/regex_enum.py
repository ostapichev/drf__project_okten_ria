from enum import Enum

from django.utils.translation import gettext_lazy as _


class RegExEnum(Enum):
    BRAND = (
        r'^[A-Z][a-zA-Z\d]{1,24}$',
        _('First letter uppercase min 2 max 24 ch')
    )

    MODEL = (
        r'^[A-Z][a-zA-Z\d]{1,24}$',
        _('First letter uppercase min 2 max 24 ch')
    )

    EMAIL = (
        r'^[\w.%+-]+@gmail\.com$',
        _('The email domain must be gmail.com')
    )

    NAME = (
        r'^[A-Z][a-zA-Z]{1,49}$',
        _('This name must contain only characters.')
    )

    SURNAME = (
        r'^[A-Z][a-zA-Z]{1,49}$',
        _('This surname must contain only characters.')
    )

    PASSWORD = (
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\'`\!@#$%\^&\*\(\)\-_=\+\|\\\/\?\.>,<])(?=.*\S)'
        r'[a-zA-Z\d\'`\!@#$%\^&\*\(\)\-_=\+\|\\\/\?\.>,<]{8,30}$',
        _('This password must be at least one uppercase letter, at least one lowercase letter, '
          'at least one special character and at least one number min 8 max 30 characters.')
    )

    CONTENT = (
        r'\b(?:fuck|dick|shit|bitch)\bgm',
        _('This content has some bad words!!!')
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg
