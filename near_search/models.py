from django.db import models

class Shop(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=100)
    photo_url = models.URLField(null=True)
    address = models.CharField(max_length=100, null=True)
    open = models.CharField(max_length=400, null=True)
    close = models.CharField(max_length=400, null=True)
    catch = models.CharField(max_length=100, null=True)
    access = models.CharField(max_length=400, null=True)
    genre_name = models.CharField(max_length=100, null=True)
    genre_catch = models.CharField(max_length=100, null=True)
    parking = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} (id: {self.id})"