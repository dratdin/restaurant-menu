from django.core.exceptions import ValidationError


class NotUniqName(ValidationError):
    pass


class CurrentCartCantBeDeleted(ValidationError):
    pass
