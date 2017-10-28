from otree.api import models, BasePlayer
from otree.db.models import Model, ForeignKey
from random import randint

#from ..models import Constants

class BaseSlider(Model):

    class Meta:
        abstract = True

    minimum = models.IntegerField(initial=0)
    maximum = models.IntegerField(initial=100)

    start_pos = models.IntegerField()
    end_pos = models.IntegerField()

    touched = models.BooleanField(initial=False)
    centered = models.BooleanField(initial=False)

    def set_starting_pos(self):
        self.start_pos = randint(self.minimum, self.maximum)

    def distance_from_center(self):
        return abs((self.minimum + self.maximum)/2 - int(self.end_pos))

    def is_centered(self):
        self.centered = self.distance_from_center() == 0
        return self.centered