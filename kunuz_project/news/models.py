from django.db import models

class News(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(unique=True)
    image = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=255, default='main')
    category = models.CharField(max_length=255, null=True, blank=True)   # YANGI QATOR
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

