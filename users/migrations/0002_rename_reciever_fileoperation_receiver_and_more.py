# Generated by Django 5.0.6 on 2024-07-02 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileoperation',
            old_name='reciever',
            new_name='receiver',
        ),
        migrations.RemoveField(
            model_name='fileoperation',
            name='operation',
        ),
    ]