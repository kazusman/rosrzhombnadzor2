from bot.config import bot
from bot.models import *
from random import randint, choice


class TextAnalyzer:

    def __init__(self, message_text, chat_id, message_id):
        self.message_text = message_text
        self.chat_id = chat_id
        self.message_id = message_id

    def _is_word_match_position(self, word_position, trigger_word) -> bool:
        word_position_matching_rules = {
            'start': self.message_text.lower().startswith(trigger_word),
            'clean_start': self.message_text.lower().startswith(f'{trigger_word} '),
            'end': self.message_text.lower().endswith(trigger_word),
            'clean_end': self.message_text.lower().endswith(f' {trigger_word}'),
            'any': trigger_word.lower() in self.message_text.lower(),
            'all': trigger_word.lower() == self.message_text.lower()
        }
        return word_position_matching_rules[word_position]

    def _is_case_sensitive_passed(self, trigger_word) -> bool:
        return trigger_word in self.message_text

    def _communicate(self, action):
        reply_to_message_id = self.message_id if action.is_need_to_reply else None
        if action.is_interpolation_needed:
            if action.answer_text.count('{}') != 1:
                return
            else:
                answer_text = action.answer_text.format(self.message_text)
        else:
            answer_text = action.answer_text
        if randint(1, 100) <= action.answer_probability:
            bot.send_message(self.chat_id, answer_text,
                             reply_to_message_id=reply_to_message_id,
                             disable_notification=action.is_need_to_send_quiet)

    def _get_rules(self, actions: list[FunnyAction]):
        actions_stat = [{'action': action, 'word_position_check': False,
                         'case_sensitive_check': True} for action in actions]
        for action in actions_stat:
            truly_action = action['action']
            word_position = truly_action.word_position
            trigger_word = truly_action.trigger_word
            is_case_sensitive = truly_action.is_case_sensitive
            action['word_position_check'] = self._is_word_match_position(word_position, trigger_word)
            if is_case_sensitive:
                action['case_sensitive_check'] = self._is_case_sensitive_passed(trigger_word)
        suitable_actions = [action['action'] for action in actions_stat if action['word_position_check']
                            and action['case_sensitive_check']]
        if suitable_actions:
            self._communicate(choice(suitable_actions))
        else:
            return

    def analyze(self):
        funny_actions = FunnyAction.objects.all()
        actions = [action for action in funny_actions if action.trigger_word.lower() in self.message_text.lower()]
        self._get_rules(actions)
