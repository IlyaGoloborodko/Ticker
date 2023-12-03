# Generated by Django 4.2.7 on 2023-12-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_text', models.TextField(max_length=100)),
                ('add_date', models.DateTimeField(verbose_name='date added')),
            ],
        ),
    ]
