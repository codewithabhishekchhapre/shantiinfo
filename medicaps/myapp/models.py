from django.db import models
from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username




class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='employee_profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    experience = models.CharField(max_length=5)
    tech = models.TextField(help_text="Comma-separated tech stack (e.g., Python, React, Django)")

    def __str__(self):
        return f"{self.user.username}'s Profile"
