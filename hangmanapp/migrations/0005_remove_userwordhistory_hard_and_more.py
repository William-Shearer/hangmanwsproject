# Generated by Django 4.2.2 on 2023-08-05 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hangmanapp', '0004_userwordhistory_won'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userwordhistory',
            name='hard',
        ),
        migrations.RemoveField(
            model_name='userwordhistory',
            name='won',
        ),
    ]
