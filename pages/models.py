from django.db import models

class AdPackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} - ${self.price}"
