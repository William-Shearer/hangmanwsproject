# Generated by Django 4.2.2 on 2023-08-18 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hangmanapp', '0011_alter_guestbook_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GuestBook',
        ),
    ]
