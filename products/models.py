from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name