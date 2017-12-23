from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Connection


class CustomPage(Page):
    def __init__(self):
        def decorate_before_next_page(original_BNP):
            def decorated_before_next_page(*args, **kwargs):
                if not self.timeout_happened:
                    new_connection = self.participant.connection_set.create(event_type='success_post')
                original_BNP(*args, **kwargs)

            return decorated_before_next_page

        def decorate_is_displayed(original_is_displayed):
            def decorated_is_displayed(*args, **kwargs):
                game_condition = original_is_displayed(*args, **kwargs)
                if Constants.players_per_group is not None:
                    return game_condition and not self.group.has_dropouts()
                else:
                    return game_condition and not self.player.is_dropout()

            return decorated_is_displayed

        super().__init__()
        setattr(self, "is_displayed", decorate_is_displayed(getattr(self, "is_displayed")))
        setattr(self, "before_next_page", decorate_before_next_page(getattr(self, "before_next_page")))


class MyPage(CustomPage):
    ...


class WP(WaitPage):
    def is_displayed(self):
        return not self.group.has_dropouts()


class Results(Page):
    def is_displayed(self):
        return not self.group.has_dropouts()


page_sequence = [
    MyPage,
    WP,
    Results
]
