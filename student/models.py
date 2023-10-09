from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    student_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        last_4_digits = self.student_id.username[-4:]
        return "{}_{}".format(self.first_name, last_4_digits)
