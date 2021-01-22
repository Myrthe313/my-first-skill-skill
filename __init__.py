from mycroft import MycroftSkill, intent_handler

class ILikeYou(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(ILikeYou.intent)
    def ILikeYou(self):

        self.speak("I really like you too!")

def create_skill():
    return ILikeYou()
