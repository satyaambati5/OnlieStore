# Generated by Django 3.1 on 2020-09-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0002_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='purchased_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
