# Generated by Django 5.0.4 on 2024-07-05 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saVex', '0005_savingsitems_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseitems',
            name='Misc',
            field=models.IntegerField(default=0),
        ),
    ]
