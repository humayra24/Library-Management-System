# Generated by Django 4.2.6 on 2023-10-05 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='department',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
    ]
