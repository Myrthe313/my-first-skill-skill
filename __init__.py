from mycroft import MycroftSkill, intent_handler

class ILikeYou(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('skill.ilikeyou.intent')
    def ILikeYou(self, message):

        self.speak("I really like you too!")

def create_skill():
    return ILikeYou()
