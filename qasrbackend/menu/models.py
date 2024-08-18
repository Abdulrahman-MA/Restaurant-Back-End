import uuid
from django.db import models
from django.core.validators import MinValueValidator


class BaseMenuItem(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.ImageField(blank=True, null=True, upload_to='uploads/menu_items/')
    description = models.CharField(max_length=2000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    class Meta:
        abstract = True

    def __str__(self):
        return self.name if self.name else "Unnamed Item"


class MenuItem(BaseMenuItem):
    CATEGORY_CHOICES = [
        ('BadoFood', 'Bado Food'),
        ('Barbeque', 'Barbeque'),
        ('Desserts', 'Desserts'),
        ('DishDay', 'Dish of the Day'),
        ('EnergyDrinks', 'Energy Drinks'),
        ('FreakShake', 'Freak Shake'),
        ('HotDrinks', 'Hot Drinks'),
        ('IceCoffee', 'Ice Coffee'),
        ('Juices', 'Juices'),
        ('Kitchen', 'Kitchen'),
        ('MilkShake', 'Milk Shake'),
        ('Pans', 'Pans'),
        ('Salads', 'Salads'),
        ('SideDishes', 'Side Dishes'),
        ('Smoothy', 'Smoothy'),
        ('Soda', 'Soda'),
        ('Tagin', 'Tagin'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    class Meta:
        db_table = 'menu_items'
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        ordering = ['name']
