import re

from rest_framework.exceptions import ValidationError


class URLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r"youtube\.com")
        my_value = dict(value).get(self.field)
        if not my_value:
            return
        if not reg.search(str(my_value)):
            raise ValidationError("Ссылка должна быть только из YouTube")
