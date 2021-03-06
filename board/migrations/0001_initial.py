# Generated by Django 3.2.7 on 2021-10-03 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherBoard',
            fields=[
                ('uniqueCode', models.CharField(max_length=5, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_id', models.IntegerField()),
                ('city_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.weatherboard')),
            ],
        ),
    ]
