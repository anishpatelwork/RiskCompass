# Generated by Django 2.1.7 on 2019-04-17 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compass', '0005_auto_20190417_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='answers',
        ),
        migrations.AddField(
            model_name='result_answer',
            name='result_answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='results_answers', to='compass.Results'),
        ),
    ]