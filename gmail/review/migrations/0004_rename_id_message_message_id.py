# Generated by Django 4.2 on 2023-05-10 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_alter_message_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='id',
            new_name='message_id',
        ),
    ]