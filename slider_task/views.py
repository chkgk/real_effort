from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

# Slider
from .models import Slider
from django.forms import modelformset_factory, HiddenInput
from otree.api import widgets


SliderFormSet = modelformset_factory(Slider, fields=('end_value', 'touched'), extra=0, widgets={'end_value': widgets.SliderInput(attrs={'step': '1'}), 'touched': HiddenInput()})


class Sliders(Page):

    def vars_for_template(self):
        sliders_query_set = Slider.objects.filter(player__exact=self.player)
        assert len(sliders_query_set) == Constants.num_sliders

        slider_formset = SliderFormSet(queryset=sliders_query_set)

        return {
            'slider_formset': slider_formset,
            'slider_values_and_forms': zip([s.start_value for s in sliders_query_set], slider_formset.forms),
            'value_list': [s.start_value for s in sliders_query_set]
        }

    def before_next_page(self):
        submitted_data = self.form.data
        slider_objs_by_id = {slider.pk: slider for slider in self.player.slider_set.all()}
        assert len(slider_objs_by_id) == Constants.num_sliders

        for i in range(Constants.num_sliders):
            input_prefix = 'form-%d-' % i

            # get the inputs
            slider_id = int(submitted_data[input_prefix + 'id'])
            end_value = submitted_data[input_prefix + 'end_value']
            touched = submitted_data[input_prefix + 'touched']

            # lookup by ID and save submitted data
            slider = slider_objs_by_id[slider_id]
            slider.end_value = end_value
            slider.touched = True if touched == "True" else False
            
            # important: save to DB!
            slider.save()


page_sequence = [
    Sliders
]
