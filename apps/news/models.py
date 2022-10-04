from django.db import models


class News(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    description = models.TextField()
    picture = models.ImageField(default=None, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.title}'
