# Generated by Django 4.2.2 on 2023-08-20 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hangmanapp', '0015_userwordhistory_date_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userwordhistory',
            name='date_done',
        ),
    ]
