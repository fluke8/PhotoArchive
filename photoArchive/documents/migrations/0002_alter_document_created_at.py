# Generated by Django 3.2.16 on 2024-12-03 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateField(),
        ),
    ]
