import json
from django.db import models
import django.core.exceptions as exceptions


class SimpleJSONTextField(models.TextField):
    """
    This field represents a JSON object (dict) which is stored in the db as a TextField but is automatically
    parsed and usuable as a dict field in the model.

    Recommended usage is: SimpleJSONTextField(null=True, blank=True)

    Null or blank (empty strings) are fine in the db but will become an empty dict {} in the model
    and will get saved out as such.

    Normally you should not assign an object as a default value directly, you must assign a separate function.
    Therefore, to make it easier to specify a "default" value, always use serialized JSON as a string.

    For example: SimpleJSONTextField(null=True, blank=True, default='{"foo":"bar"}')
    """

    default_error_messages = {
        'invalid': "'%(value)s' is not valid JSON.",
    }
    description = 'JSON data'
    empty_strings_allowed = True

    def __init__(self, verbose_name=None, default=None, **kwargs):
        self._default_json_str = default
        if default:
            kwargs['default'] = self.default_json_value
        super().__init__(verbose_name, **kwargs)

    def default_json_value(self):
        return json.loads(self._default_json_str)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if 'default' in kwargs:
            kwargs['default'] = self._default_json_str
        return name, path, args, kwargs

    def get_internal_type(self):
        return "TextField"

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if isinstance(value, dict):
            value = json.dumps(value)
        elif not isinstance(value, str):
            raise ValueError('SimpleJSONField value must be a dict or string')
        return value

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return {}
        if isinstance(value, str):
            try:
                if value:
                    return json.loads(value)
                else:
                    return {}
            except ValueError:
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value

    def value_from_object(self, obj):
        """
        Called from value_to_string() as well as whatever gets the text to display in the admin form fields.
        The super() implementation returns the value of this field in the given model instance.
        We convert it to a JSON string for use in form fields.
        """
        value = super().value_from_object(obj)
        return self.get_db_prep_value(value, None)
