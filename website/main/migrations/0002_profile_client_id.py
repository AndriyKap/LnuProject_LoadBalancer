# Generated by Django 4.2.5 on 2023-11-08 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='client_id',
            field=models.IntegerField(null=True),
        ),
    ]
