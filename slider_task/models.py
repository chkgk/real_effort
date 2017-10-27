from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


from otree.db.models import Model, ForeignKey
import random

author = 'Christian König'

doc = """
A simple slider task
"""


class Constants(BaseConstants):
    name_in_url = 'slider_task'
    players_per_group = None
    num_rounds = 1

    num_sliders = 5



class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.prepare_sliders()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def prepare_sliders(self):
        """
        Sliders are initialized with a starting value. Values are different by participants at the moment.
        Could be improved to have same starting values for all players.
        Could also be loaded from file to have the same starting values in all sessions.
        """
        for _ in range(Constants.num_sliders):
            slider = self.slider_set.create()
            slider.start_value = random.randint(0, 100)
            slider.save()



class Slider(Model):
    minimum = 0
    maximum = 100

    start_value = models.IntegerField(min=minimum, max=maximum)
    end_value = models.IntegerField(min=minimum, max=maximum)
    touched = models.BooleanField(initial=False)
    player = ForeignKey(Player)