from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
from datetime import date


class Result(models.Model):
    date = models.DateField()
    player_1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='player_1')

    player_2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='player_2')

    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='winner')

    def clean(self):

        if self.date > date.today():
            raise ValidationError('Seems like this match happened in future. Date of the match > current time ')

        if self.player_1 == self.player_2:
            raise ValidationError('Player 1 and Player 2 are the same.')
        
        if self.winner not in [self.player_1, self.player_2]:
            raise ValidationError('Winner didnt participate in this match.')
