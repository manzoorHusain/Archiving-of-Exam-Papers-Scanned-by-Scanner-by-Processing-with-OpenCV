from django.db import models

# Create your models here.


class Sinav(models.Model):
    bolum = models.CharField(max_length=200)
    ders = models.CharField(max_length=200)
    sinav_tipi = models.CharField(max_length=200)
    tc = models.BigIntegerField(primary_key=True, max_length=11)

    class Meta:
        unique_together = (('ders', 'sinav_tipi', 'tc'))
