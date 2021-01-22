import time
from datetime import datetime, timedelta
from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_duration, extract_number
from mycroft.util.time import now_local


class ILikeYou(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(ILikeYou.intent)
    def ILikeYou(self):

        self.speak("I really like you too!")

def create_skill():
    return ILikeYou()
