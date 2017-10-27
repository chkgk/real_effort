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

    # slider config 
    num_sliders = 50

    slider_columns = 3 # optional
    slider_range = (0, 100) # optional




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
            slider = self.slider_set.create()
            slider.set_starting_pos()
            slider.save()


    def count_centered_sliders(self):
        sum_centered = 0
        sliders = Slider.objects.filter(player__exact=self)
        for s in sliders:
            if s.touched and s.centered:
                sum_centered += 1

        self.centered_sliders = sum_centered


class Slider(Model):
    if hasattr(Constants, 'slider_range'):
        if not Constants.slider_range[1] > Constants.slider_range[0]:
            raise Exception("the first element of slider range must be smaller than second element.")

        if not (Constants.slider_range[1]-Constants.slider_range[0]) % 2 == 0:
            raise Exception("slider range must result in an uneven number of possible positions.")

        slider_min = Constants.slider_range[0]
        slider_max = Constants.slider_range[1] 
    else:
        slider_min = 0
        slider_max = 100

    minimum = models.IntegerField(initial=slider_min)
    maximum = models.IntegerField(initial=slider_max)

    start_pos = models.IntegerField()
    end_pos = models.IntegerField()

    touched = models.BooleanField(initial=False)
    centered = models.BooleanField(initial=False)

    player = ForeignKey(Player)

    def set_starting_pos(self):
        self.start_pos = random.randint(self.minimum, self.maximum)

    def distance_from_center(self):
        return abs((self.minimum + self.maximum)/2 - int(self.end_pos))

    def is_centered(self):
        self.centered = self.distance_from_center() == 0
        return self.centered

