# Generated by Django 3.2.20 on 2023-08-29 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('category', models.CharField(default='', max_length=60)),
                ('subcategory', models.CharField(default='', max_length=60)),
                ('price', models.IntegerField(default=0)),
                ('desc', models.CharField(max_length=250)),
                ('image', models.ImageField(upload_to='shop/images')),
            ],
        ),
    ]
