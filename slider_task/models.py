from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


from otree.db.models import Model, ForeignKey
import random


from .slider.models import BaseSlider


author = 'Christian König'

doc = """
A simple slider task
"""


class Constants(BaseConstants):
    name_in_url = 'slider_task'
    players_per_group = None
    num_rounds = 1

    # slider config 
    num_sliders = 50

    slider_columns = 3 # optional



class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.prepare_sliders()


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    centered_sliders = models.PositiveIntegerField()

    def prepare_sliders(self):
        """
        Sliders are initialized with a starting value. Values are different by participants at the moment.
        Could be improved to have same starting values for all players.
        Could also be loaded from file to have the same starting values in all sessions.
        Set steps / acceptance area (precision needed for receiving payoff)
        could also specify requirements for payoff (dead on middle, within interval around middle,
        distance from center etc.)
        """
        for _ in range(Constants.num_sliders):
            slider = Slider()
            slider.player = self
            slider.set_starting_pos()
            slider.save()


    def count_centered_sliders(self):
        sum_centered = 0
        sliders = Slider.objects.filter(player__exact=self)
        for s in sliders:
            if s.touched and s.centered:
                sum_centered += 1

        self.centered_sliders = sum_centered


class Slider(BaseSlider):
    player = ForeignKey(Player)
    minimum = 0
    maximum = 1000


# class SliderSet:
#     def __init__(self, player, num_sliders, slider_range=(0, 100)):
#         for _ in num_sliders:
#             slider = Slider()
#             slider.player = player
#             slider.minimum = slider_range[0]
#             slider.maximum = slider_range[1]
#             slider.set_starting_pos()
#             slider.save()
