# Generated by Django 4.2.5 on 2023-11-18 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_belltask_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='belltask',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
