# Generated by Django 2.1.7 on 2019-05-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compass', '0002_auto_20190501_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='employee',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]