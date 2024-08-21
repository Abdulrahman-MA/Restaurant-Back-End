from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, default=None)
    subcategories = models.BooleanField(default=False)
    image_path = models.ImageField(default='uploads/categories/')

    def __str__(self):
        return self.name


class Subcategory (models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.name})-->({self.category})'


class BaseMenuItem(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    description = models.TextField(max_length=2000, blank=True, null=True)

    half_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     validators=[MinValueValidator(0.01)], default=00.00)

    third_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      validators=[MinValueValidator(0.01)], default=00.00)

    quart_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      validators=[MinValueValidator(0.01)], default=00.00)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')
    image_path = models.ImageField(default='uploads/menu_items/', upload_to=f'uploads/menu_items/{category}')
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


@receiver(post_delete, sender=MenuItem)
def delete_image_file(sender, instance, **kwargs):
    instance.image_path.delete(False)
