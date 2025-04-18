from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username
