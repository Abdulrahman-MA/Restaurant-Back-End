# Generated by Django 5.1 on 2024-08-21 06:08

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_remove_menuitem_item_id_alter_menuitem_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='menu.category'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='image_path',
            field=models.ImageField(default='uploads/menu_items/', upload_to='uploads/menu_items/<django.db.models.fields.related.ForeignKey>'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]
