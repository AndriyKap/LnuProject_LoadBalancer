# Generated by Django 4.2.5 on 2023-11-13 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_belltask_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='belltask',
            name='result',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='belltask',
            name='value',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
