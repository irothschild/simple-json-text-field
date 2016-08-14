# simple-json-text-field

A simple JSON TextField for Django models.

This field represents a JSON object (dict) which is stored in the db as a `TextField` but is automatically
parsed and usable as a dict field in the model.

Example usage is:

```
my_field = SimpleJSONTextField(null=True, blank=True)
```

Null or blank (empty strings) are fine in the db but will become an empty dict `{}` in the model
and will get saved out as such.

Normally you should not assign an object as a default value directly, you must assign a separate function.
Therefore, to make it easier to specify a `default` value, always use serialized JSON as a string.

For example:

```
my_field = SimpleJSONTextField(default='{"foo":"bar"}')
```

In the Django admin console, the JSON field will appear as a text field where you can enter JSON data and the syntax is verified before saving.

## Example

```
from django.db import models
from .fields import SimpleJSONTextField

class MyModel(models.Model):
    foobar = SimpleJSONTextField(null=True, blank=True)

mine = MyModel.objects.get_or_create(foobar={"simple": "it works"})
print(mine.foobar['simple'])
```


## Why?

There are some other JSON fields for Django including JSONField in Django 1.9 that only supports PostgreSQL and various
other modules which have been around for a while, have somewhat complicated code that includes support for legacy
versions of Django, and have numerous open issues and pull requests.

The SimpleJSONTextField is:

- tiny and simple
- written for Django 1.10 (should work for 1.9)
- treated as text in the db so should work with any Django-supported database
- written for Python 3 (of course!)


# License

Free to use with an [MIT License](LICENSE)
