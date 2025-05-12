from django.db import models


from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    # extrafields
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username