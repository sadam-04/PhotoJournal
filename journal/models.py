from django.db import models
from django.utils import timezone

# Create your models here.
class JournalEntry(models.Model):
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=1024)