# Generated by Django 5.1 on 2024-08-22 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0014_alter_category_image_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image_path',
            field=models.ImageField(default='uploads/menu_items/', upload_to=''),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='image_path',
            field=models.ImageField(default='uploads/menu_items/', upload_to=''),
        ),
    ]
