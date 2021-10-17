from django.db import models
from django.conf import settings

# Create your models here.




class Exercise(models.Model):
    name=models.CharField(max_length=100)
    userId= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    hintsTotal= models.IntegerField()
    hintsFound= models.IntegerField()
    time= models.FloatField()