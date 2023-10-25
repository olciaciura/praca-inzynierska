from django.db import models

class DataModel(models.Model):
    file = models.ImageField(upload_to='')
