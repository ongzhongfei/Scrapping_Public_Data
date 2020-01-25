# Generated by Django 2.1.7 on 2020-01-23 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tenure_raw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenure', models.CharField(max_length=128)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('rate', models.FloatField()),
            ],
        ),
    ]