# Generated by Django 4.1.5 on 2023-02-13 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='description',
            name='detail',
            field=models.TextField(verbose_name='جزئیات'),
        ),
    ]
