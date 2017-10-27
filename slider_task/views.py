from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

# Slider
from .models import Slider
from django.forms import modelformset_factory, HiddenInput
from otree.api import widgets
from math import ceil
from random import randint

SliderFormSet = modelformset_factory(Slider, fields=('end_pos', 'touched'), extra=0)


class Sliders(Page):

    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def vars_for_template(self):
        sliders_query_set = Slider.objects.filter(player__exact=self.player)
        assert len(sliders_query_set) == Constants.num_sliders

        slider_formset = SliderFormSet(queryset=sliders_query_set)

        # starting_values = [s.start_pos for s in sliders_query_set]
        # min_values = [s.minimum for s in sliders_query_set]
        # max_values = [s.maximum for s in sliders_query_set]
        # offsets = [randint(0, 10) for _ in sliders_query_set]

        starting_values = []
        min_values = []
        max_values = []
        offsets = []
        for s in sliders_query_set:
            starting_values.append(s.start_pos)
            min_values.append(s.minimum)
            max_values.append(s.maximum)
            offsets.append(randint(0, 10))


        if hasattr(Constants, 'slider_columns'):
            if Constants.slider_columns > 0:
                slider_columns = Constants.slider_columns
        else:
            slider_columns = 1

        chunk_size = ceil(Constants.num_sliders / slider_columns)

        return {
            'slider_formset': slider_formset,
            'slider_values_and_forms': list(self._chunks(list(zip(offsets, min_values, max_values, starting_values, slider_formset.forms)), chunk_size)),
            'slider_columns': slider_columns
        }

    def before_next_page(self):
        submitted_data = self.form.data
        slider_objs_by_id = {slider.pk: slider for slider in self.player.slider_set.all()}
        assert len(slider_objs_by_id) == Constants.num_sliders

        for i in range(Constants.num_sliders):
            input_prefix = 'form-%d-' % i

            slider_id = int(submitted_data[input_prefix + 'id'])
            end_pos = submitted_data[input_prefix + 'end_pos']
            touched = submitted_data[input_prefix + 'touched']

            slider = slider_objs_by_id[slider_id]
            slider.end_pos = end_pos
            slider.touched = True if touched == "True" else False
            slider.save()

            slider.is_centered()
            slider.save()

        self.player.count_centered_sliders()


page_sequence = [
    Sliders
]
