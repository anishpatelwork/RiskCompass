# Generated by Django 2.2.1 on 2019-05-01 10:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('score', models.IntegerField(default=0)),
                ('recommendation', models.TextField(default='Contact Anish Patel for more information')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='compass.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='Exceedance', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Quiz',
            },
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('company', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'User Details',
            },
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('quiz', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='quizresults', to='compass.Quiz')),
                ('userdetails', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='compass.UserDetails')),
            ],
            options={
                'verbose_name_plural': 'Results',
            },
        ),
        migrations.CreateModel(
            name='Question_choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_answers', to='compass.Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results_answers', to='compass.Question')),
                ('question_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results_answers', to='compass.Results')),
            ],
            options={
                'verbose_name_plural': 'Result Answers',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='compass.Quiz'),
        ),
        migrations.CreateModel(
            name='Business_Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=1, max_digits=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_priority', to='compass.Category')),
                ('results', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='business_priority', to='compass.Results')),
            ],
            options={
                'verbose_name_plural': 'Business Priorities',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='compass.Question'),
        ),
    ]
