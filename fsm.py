from random import randint
from time import clock


##===================== ROBOT FSM EXAMPLES ==============##
# Transitions

# States
#### CleanDishes
#### Vacuum
#### Sleep

# FSM

# Character
#### Robot Maid

# Main Code


##===================== TRANSITIONS =====================##
class Transition(object):
    def __init__(self, to_state):
        self.to_state = to_state

    def execute(self):
        print("Transitioning...")


##===================== STATES =====================##
class State(object):
    def __init__(self, fsm):
        self.FSM = fsm
        self.timer = 0
        self.start_time = 0

    def enter(self):
        self.timer = randint(0, 5)
        self.start_time = int(clock())

    def execute(self):
        pass

    def exit(self):
        pass


class Clean_Dishes(State):
    def __init__(self, fsm):
        super(Clean_Dishes, self).__init__(fsm)

    def enter(self):
        print("Preparing to clean dishes")
        return super(Clean_Dishes, self).enter()

    def execute(self):
        print("Cleaning dishes")
        if self.start_time + self.timer <= clock():
            if not (randint(1, 3) % 2):
                self.FSM.to_transition("to_vacuum")
            else:
                self.FSM.to_transition("to_sleep")

    def exit(self):
        print("Finished cleaning dishes")


class Vacuum(State):
    def __init__(self, fsm):
        super(Vacuum, self).__init__(fsm)

    def enter(self):
        print("Preparing to vacuum")
        return super(Vacuum, self).enter()

    def execute(self):
        print("Vacuuming")
        if (self.start_time + self.timer <= clock()):
            if not (randint(1, 3) % 2):
                self.FSM.to_transition("to_sleep")
            else:
                self.FSM.to_transition("to_clean_dishes")

    def exit(self):
        print("Finished vacuuming")


class Sleep(State):
    def __init__(self, fsm):
        super(Sleep, self).__init__(fsm)

    def enter(self):
        print("Preparing to sleep")
        return super(Sleep, self).enter()

    def execute(self):
        print("Sleeping")
        if self.start_time + self.timer <= clock():
            if not (randint(1, 3) % 2):
                self.FSM.to_transition("to_vacuum")
            else:
                self.FSM.to_transition("to_clean_dishes")

    def exit(self):
        print("Waking up from sleep")


##===================== FINITE STATE MACHINES =====================##
class FSM(object):
    def __init__(self, character):
        self.character = character
        self.states = {}
        self.transitions = {}
        self.current_state = None
        self.previous_state = None
        self.trans = None

    def add_transition(self, transition_name, transition):
        self.transitions[transition_name] = transition

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def set_state(self, state_name):
        self.previous_state = self.current_state
        self.current_state = self.states[state_name]

    def to_transition(self, to_trans):
        self.trans = self.transitions[to_trans]

    def execute(self):
        if self.trans:
            self.current_state.exit()
            self.trans.execute()
            self.set_state(self.trans.to_state)
            self.current_state.enter()
            self.trans = None
        else:
            # print("An error occurred")
            self.current_state.execute()


##===================== IMPLEMENTATION =====================##
Maid = type("Maid")


class Robot_Maid(Maid):
    def __init__(self):
        self.FSM = FSM(self)

        ##STATES
        self.FSM.add_state("Sleep", Sleep(self.FSM))
        self.FSM.add_state("Clean_Dishes", Clean_Dishes(self.FSM))
        self.FSM.add_state("Vacuum", Vacuum(self.FSM))

        ##TRANSITIONS
        self.FSM.add_transition("to_sleep", Transition("Sleep"))
        self.FSM.add_transition("to_vacuum", Transition("Vacuum"))
        self.FSM.add_transition("to_clean_dishes", Transition("Clean_Dishes"))

        self.FSM.set_state("Sleep")

    def execute(self):
        self.FSM.execute()


if __name__ == '__main__':
    r = Robot_Maid()
    for i in range(10):
        start_time = clock()
        time_interval = 1
        while start_time + time_interval > clock():
            pass
        r.execute()
