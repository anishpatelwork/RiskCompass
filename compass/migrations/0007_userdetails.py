# Generated by Django 2.1.7 on 2019-03-21 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compass', '0006_auto_20180415_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(default='')),
                ('last_name', models.TextField(default='')),
                ('company', models.TextField(default='')),
                ('sector', models.TextField(default='')),
                ('email', models.TextField(default='')),
                ('role', models.TextField(default='')),
                ('rmb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_details', to='compass.RMB')),
            ],
        ),
    ]
