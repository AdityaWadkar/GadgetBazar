# Generated by Django 3.2.20 on 2023-09-02 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0005_auto_20230901_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='name',
            new_name='fname',
        ),
        migrations.AddField(
            model_name='orders',
            name='lname',
            field=models.CharField(default='', max_length=50),
        ),
    ]
