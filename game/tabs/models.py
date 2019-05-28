from django.db import models
from django.conf import settings
# Create your models here.
class Result(models.Model):
    date     = models.DateField()
    player_1 =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='player_1'
    )
    player_2 =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='player_2'
    )
    winner =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='winner'
    )