import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.forms import Textarea


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, default=None)
    subcategories = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Subcategory (models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.name})-->({self.category})'


class BaseMenuItem(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.ImageField(blank=True, null=True, upload_to='uploads/menu_items/')
    description = models.TextField(max_length=2000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)],)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name if self.name else "Unnamed Item"


class MenuItem(BaseMenuItem):

    class Meta:
        db_table = 'menu_items'
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        ordering = ['name']
