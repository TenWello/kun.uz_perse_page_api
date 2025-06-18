from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(unique=True)
    image = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=255, default='main')
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
