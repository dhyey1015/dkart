# Generated by Django 5.1 on 2024-08-20 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_alter_cartitem_cart_alter_cartitem_variations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
