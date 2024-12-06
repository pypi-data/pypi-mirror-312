# Django Model Admin Fields

[Django](https://www.djangoproject.com/) is one of the most popular Python web frameworks today. Importantly, it provides an [ORM](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) permitting us to define models as Python classes that Django maps to a database representations for us. 

A very common, nearly ubiquitous desire/need I have is to keep some record against all database objects as to who created them, when and who last edited them and when. Very basic tracking fields. Given the ubiquity of the need it was best implemented as an abstract model that my models derive from.

The basic Django example of model:

```python
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

can be extended thusly:

```python
from django.db import models
from django_model_admin_fields import AdminModel

class Person(AdminModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

which has the simple effect of adding the following fields to the model silently:

```python
    created_by = models.ForeignKey(User, verbose_name='Created By', 
                                   related_name='%(class)ss_created', 
                                   editable=False, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField('Time of Creation', editable=False, null=True)
    created_on_tz = TimeZoneField('Time of Creation, Timezone', 
                                  default=settings.TIME_ZONE, editable=False)

    last_edited_by = models.ForeignKey(User, verbose_name='Last Edited By', 
                                       related_name='%(class)ss_last_edited', 
                                       editable=False, null=True, on_delete=models.SET_NULL)
    last_edited_on = models.DateTimeField('Time of Last Edit', editable=False, null=True)
    last_edited_on_tz = TimeZoneField('Time of Last Edit, Timezone', 
                                      default=settings.TIME_ZONE, editable=False)
```

(a more precise description of course is in `__init__.py`)

Importantly it also overrides the model's `save()` method to set those six fields before calling `super().save()` (i.e. the default save method) and thus these fields are automatically managed.

The [currently active](https://docs.djangoproject.com/en/3.2/topics/i18n/timezones/#selecting-the-current-time-zone) Django timezone is saved as well to support sensible human interpretation of the saved times (as Django's [DateTimeField](https://docs.djangoproject.com/en/3.2/ref/models/fields/#datetimefield)) is not timezone aware.

To make use of that easier, two properties are also added to the model: `created_on_local` and `last_edited_on_local` which are timezone aware versions of the naive `created_one` and `last_edited_on` fields.

To illustrate use of the Person example above:

```Python
person = Person()
person.first_name = "John"
person.last_name = "Smith"
person.save

print(f"{person.first_name} {person.last_name}")
print(f"was created by {person.created_by} on {person.created_on_local}.")
```

Of course to make use of local times, you need to activate the timezone that the creating user is in. To do that you need to know it first. The JavaScript library [jstz](https://github.com/iansinnott/jstz) is useful in that regard for detecting the users timezone and there's a great guide on [setting timezones](https://docs.djangoproject.com/en/3.2/topics/i18n/timezones/#selecting-the-current-time-zone) in Django in the Django documentation proper.

