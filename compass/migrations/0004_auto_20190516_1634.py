# Generated by Django 2.2.1 on 2019-05-16 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compass', '0003_userdetails_employee'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Business_Priority',
            new_name='BusinessPriority',
        ),
        migrations.RenameModel(
            old_name='Question_choice',
            new_name='QuestionChoice',
        ),
    ]