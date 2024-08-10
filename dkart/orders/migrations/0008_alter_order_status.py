# Generated by Django 5.0.8 on 2024-08-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_orderproduct_color_remove_orderproduct_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Completed', 'Completed'), ('New', 'New'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]
