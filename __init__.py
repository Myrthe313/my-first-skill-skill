import time
from datetime import datetime, timedelta
from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_duration, extract_number
from mycroft.util.time import now_local


class MyFirstSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.task_names = ['task one', 'task two', 'task three']
        self.block_names = ['one block', 'two blocks', 'three blocks']
        self.participant_number = None
        self.tasks = []
        self.blocks = None

    def get_participant_number(self):
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
        if correct_number == 'no':
            self.speak("Sorry I must have misunderstood you. Let's try again.")
            return self.get_participant_number()
        elif correct_number == 'yes':
            self.speak("Great, let's move on!")
            return self.participant_number

    def create_a_task(self, dialog_file, task_ordinal):

        task = self.get_response(dialog_file)
        self.speak("You have chosen {} as your {} task for this study session.".format(task, task_ordinal))

        confirmation = self.ask_yesno('tasks.confirmation', data={"task": task, "task_ordinal": task_ordinal})
        while confirmation != 'yes' and confirmation != 'no':
            self.speak("I am sorry but I did not understand you. Please answer with yes or no.")
            confirmation = self.ask_yesno('tasks.confirmation', data={"task": task, "task_ordinal": task_ordinal})
        if confirmation == 'no':
            self.speak("I must have misunderstood you, let's try again.")
            return self.create_a_task(dialog_file, task_ordinal)
        elif confirmation == 'yes':
            return task

    def get_tasks(self):

        self.speak("In order to make this session more productive and for me to be more helpful " +
                   "I would like to know the tasks you want to accomplish.")

        tasks = []
        task1 = self.create_a_task('tasks.task1', "first")
        tasks.append(task1)

        # Get the second task the user wants to accomplish
        another_task = self.ask_yesno('tasks.another.task')
        while another_task != 'yes' and another_task != 'no':
            self.speak("I am sorry but I did not understand you. Please answer with yes or no.")
            another_task = self.ask_yesno('tasks.another.task')
        if another_task == "yes":
            task2 = self.create_a_task('tasks.task2', "second")
            tasks.append(task2)
        elif another_task == "no":
            self.speak("That is okay, lets's move on!")
            return tasks

        # Get the third task the user wants to accomplish
        last_task = self.ask_yesno('tasks.last.task')
        while last_task != 'yes' and last_task != 'no':
            self.speak("I am sorry but I did not understand you. Please answer with yes or no.")
            last_task = self.ask_yesno('tasks.last.task')
        if last_task == "yes":
            task3 = self.create_a_task('tasks.task3', "third")
            tasks.append(task3)
            return tasks
        elif last_task == "no":
            self.speak("That is okay, let's move on!")
            return tasks

    def completion_of_tasks(self, tasks):

        for i in range(len(tasks)):

            task = tasks[i]
            task_number = i + 1
            completed_task = self.ask_yesno('tasks.completed.task', data={"task": task,
                                                                          "task_number": task_number})
            while completed_task != 'yes' and completed_task != 'no':
                self.speak("I am sorry but I did not understand you. Please respond with yes or no.")
                self.ask_yesno('tasks.completed.task', data={"task": task,
                                                             "task_number": task_number})
            if completed_task == 'yes':
                self.speak("Great job!")
            elif completed_task == 'no':
                self.speak("That is okay, you can always consider another studying session.")

    def get_blocks(self, block_names):

        self.speak("In this study session, we will make use of the pomodoro technique." +
                   " During the session you will have study blocks of 25 minutes with " +
                   "a break of 5 minutes between blocks." +
                   " For this session, do you want to study for:")
        blocks = extract_number(self.ask_selection(block_names, 'blocks.selection'))
        while not blocks:
            self.speak("Sorry, I could not understand you." +
                       " Do you want to study for one block, two blocks or three blocks?")
            blocks = extract_number(self.ask_selection(block_names, 'skill.blocks.could.not.understand'))

        return blocks

    def blocks_confirmation(self, blocks):

        # If the user selects one block, Mycroft responds with the singular "block"
        if blocks == 1:
            amount_of_blocks = "1 block"

        # If the user selects multiple blocks, Mycroft responds with the plural "blocks"
        if blocks > 1:
            amount_of_blocks = "{} blocks".format(str(blocks))

        # Get the current time to calculate the time when the user will be done in the future
        now = now_local()
        current_time = now.strftime("%H:%M")

        # Calculate the time when the user is done based on the amount of blocks selected
        # Each block is 25 minutes and each break is 5 minutes

        minutes = blocks * 25 + (blocks - 1) * 5
        future_time = now + timedelta(minutes=minutes)
        future_time = future_time.strftime("%H:%M")

        # Respond to the user with the amount of blocks they have chosen, what the curren time is
        # and when their study session will be finished
        self.speak_dialog('blocks.confirmation', data={'currenttime': current_time,
                                                       'amount_of_blocks': amount_of_blocks,
                                                       'futuretime': future_time})

    def study_time(self, blocks):

        # The time.sleep() function takes an input of seconds
        # If you want the code to sleep for several minutes you should multiply the values with 60
        # Currently everythting is in second for debugging purposes
        for i in range(blocks):
            time.sleep(25)
            if i < blocks - 1:
                self.speak("You have been busy for quite some time now. Let’s take a well deserved 5 minute break, enjoy!")
                time.sleep(5)
                self.speak_dialog("Your break is over, hopefully you enjoyed and are now refreshed to start studying again.")
            if i == blocks - 1:
                break
        self.speak("You have finished your studying session. Well done!" +
                   "Let's see what tasks you were able to accomplish during your studying session.")

    @intent_handler('skill.study.intent')
    def handle_skill_study(self, message):
        
        # Give a welcome message to the user
        self.speak("Welcome to your study session, good to see you!" +
                   " I will be your personal assistant and help you during your studies." +
                   " Let’s start working together!" +
                   " Before we begin with the study session, we will first need to do some set up.")

        # Get the participant number from the user using the get_participant_number() function
        self.participant_number = self.get_participant_number()
        print(self.participant_number)

        # Get the tasks the user wants to accomplish
        self.tasks = self.get_tasks()
        print(self.tasks)

        self.speak("Now that I know the tasks you want to accomplish, let's decide how long you are willing to study.")

        # Get the amount of blocks from the user
        self.blocks = self.get_blocks(self.block_names)

        # Confirm the total study time of the session
        self.blocks_confirmation(self.blocks)

        # Begin study session
        self.study_time(self.blocks)

        # Ask about completion of tasks
        self.completion_of_tasks(self.tasks)

        # End of study session
        self.speak("This is the end of your study session. You did a great job! Enjoy your time off!")

def create_skill():
    return MyFirstSkill()
