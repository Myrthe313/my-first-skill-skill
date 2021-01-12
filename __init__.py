import time
from datetime import datetime, timedelta
from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_duration, extract_number
from mycroft.util.time import now_local



class MyFirstSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.tasknames = ['task one', 'task two', 'task three']
        self.blocks = ['one block', 'two blocks', 'three blocks']
        self.participant_number = 999

    def get_participant_number(self, message):
        """This function requests the user's participant number. If the user responds with the wrong number
           the function will recursively call on itself in order to redo the process."""

        # Get the participant number from the user
        self.participant_number = self.get_response('skill.participant.number')

        # Make sure the participant number from the user is correct
        correct_number = self.ask_yesno('skill.participant.number.confirmation',
                                                    data={"participant_number": self.participant_number})
        while correct_number != 'yes' and correct_number != 'no':
            self.speak("I am sorry but I did not understand you.")
            correct_number = self.ask_yesno('skill.participant.number.confirmation')
        if correct_number == 'yes':
            self.speak("Great, let's move on!")
            return self.participant_number
        elif correct_number == 'no':
            self.speak("Sorry I must have misunderstood you before. Let's try again.")
            self.get_participant_number()

    @intent_handler('skill.study.intent')
    def handle_skill_study(self, message):
        
        # Give a welcome message to the user
        self.speak("Welcome to your study session!" +
                   " I will be your personal assistant and help you during your studies." +
                   " Before we begin with the study session, we will first need to do some set up.")

        # Get the participant number from the user using the get_participant_number() function
        self.participant_number = self.get_participant_number()

        # Get the tasks the user wants to accomplish
        tasks = []
        task1 = self.get_response('tasks.task1')
        self.speak("You have chosen {} as your first task for this study session.".format(task1) +
                   " If you want to change the name for task one, say change a task")
        tasks.append(task1)

        # Get the second task the user wants to accomplish
        another_task = self.ask_yesno('tasks.another.task')
        while another_task != 'yes' and another_task != 'no':
            self.speak("I am sorry but I did not understand you. Please answer with yes or no.")
            another_task = self.ask_yesno('tasks.another.task')
        if another_task == "yes":
            task2 = self.get_response('tasks.task2')
            tasks.append(task2)
        elif another_task == "no":
            self.speak("Ok let's move on.")

        # Get the third task the user wants to accomplish
        last_task = self.ask_yesno('tasks.last.task')
        while last_task != 'yes' and last_task != 'no':
            self.speak("I am sorry but I did not understand you. Please answer with yes or no.")
            last_task = self.ask_yesno('tasks.last.task')
        if last_task == "yes":
            task3 = self.get_response('tasks.task3')
            tasks.append(task3)
        elif last_task == "no":
            self.speak("Ok let's move on.")

        if len(tasks) == 1:
            number_of_tasks = "1 task"
        if len(tasks) > 1:
            number_of_tasks = "{} tasks".format(len(tasks))

        self.speak_dialog('tasks.confirmation', data={"number_of_tasks": number_of_tasks})

        # Get the amount of blocks from the user
        #blocks = self.get_response('blocks.amount.of.blocks')
        self.speak_dialog("Now that I know the tasks you want to accomplish, let's decide how long you want to study." +
                          " Each block will last 25 minutes and every break is 5 minutes." +
                          " How many blocks do you want to study?")
        blocks = extract_number(self.ask_selection(self.blocks, 'blocks.selection'))
        while not blocks:
            self.speak("Sorry, I could not understand you." +
                       " Do you want to study one block, two blocks or three blocks?" +
                       " Please respond by choosing one of the options.")
            blocks = extract_number(self.ask_selection(self.blocks, 'skill.blocks.could.not.understand'))

        # If the user selects one block, Mycroft responds with the singular "block" 
        if blocks == 1:
            amount_of_blocks = "1 block"
        
        # If the user selects multiple blocks, Mycroft responds with the plural "blocks"
        if blocks > 1:
            amount_of_blocks = "{} blocks".format(str(blocks))
            
        # Get the current time to calculate the time when the user will be done in the future
        now = now_local()
        currenttime = now.strftime("%H:%M")
        
        # Calculate the time when the user is done based on the amount of blocks selected
        # Each block is 25 minutes and each break is 5 minutes
        
        minutes = blocks*25 + (blocks-1)*5
        futuretime = now + timedelta(minutes=minutes)
        futuretime = futuretime.strftime("%H:%M")
        
        # Respond to the user with the amount of blocks they have chosen, what the curren time is
        # and when their study session will be finished
        self.speak_dialog('blocks.confirmation', data={'currenttime': currenttime,
                                                        'amount_of_blocks': amount_of_blocks,
                                                        'futuretime': futuretime})

        
        # The time.sleep() function takes an input of seconds
        # If you want the code to sleep for several minutes you should multiply the values with 60
        # Currently everythting is in second for debugging purposes
        for i in range(blocks):
            time.sleep(25)
            if i <  blocks-1:
                self.speak("It's time for a 5 minute break")
                time.sleep(5)
                self.speak_dialog("Ok, break time is over. Get back to work.")
            if i == blocks-1:
                break
        self.speak("You have finished your studying session." +
                   " Let's see what tasks you were able to accomplish during your studying session.")

        # Ask about completion of tasks

        for i in range(len(tasks)):

            task = tasks[i]
            task_number = i + 1
            completed_task = self.ask_yesno('tasks.completed.task', data={"task": task,
                                                                          "task_number": task_number})
            while completed_task != 'yes' and completed_task != 'no':
                self.speak("I am sorry but I did not understand you. Please respond with yes or no.")
            if completed_task == 'yes':
                self.speak("Great job!")
            elif completed_task == 'no':
                self.speak("I am very disappointed, please consider another studying session.")

    @intent_handler('tasks.change.task.intent')
    def change_task(self, message):
        selection = self.ask_selection(self.tasknames, 'tasks.what.task')

        if selection == 'task one':
            task1 = self.get_response('tasks.change.task', data={"selection": selection})
            self.speak_dialog('tasks.task1.confirmation', data={"task1": task1})

        if selection == 'task two':
            task2 = self.get_response('tasks.change.task', data={"selection": selection})
            self.speak_dialog('tasks.task2.confirmation', data={"task2": task2})

        if selection == 'task three':
            task3 = self.get_response('tasks.change.task', data={"selection": selection})
            self.speak_dialog('tasks.task3.confirmation', data={"task3": task3})

def create_skill():
    return MyFirstSkill()
