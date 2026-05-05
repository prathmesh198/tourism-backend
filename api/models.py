from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
