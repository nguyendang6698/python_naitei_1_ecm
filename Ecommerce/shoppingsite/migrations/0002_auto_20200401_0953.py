# Generated by Django 3.0.2 on 2020-04-01 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='profile_default.png', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='category_default.png', upload_to='category_pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_default.png', upload_to='product_pics'),
        ),
    ]
