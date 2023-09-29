from django.core import validators
from django.core.exceptions import ValidationError

class Validator:

    @staticmethod
    def validate_input(username, reponame, timezone):
        Validator.validate_usename_reponame(username, reponame)
        Validator.validate_timezone(timezone)

    @staticmethod
    def validate_usename_reponame(username, reponame):
        try:
            validators.validate_slug(username)
            validators.validate_slug(reponame)
        except ValidationError:
            raise ValidationError("Username or repo name are not valid")    

    @staticmethod
    def validate_timezone(timezone):
        if timezone not in ["America/Montreal"]:
            raise ValidationError("Timezone is not valid")