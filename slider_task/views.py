from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

# SliderTaskPage
from .slider.pages import SliderTaskPage


class Sliders(SliderTaskPage):
    pass


page_sequence = [
    Sliders
]
