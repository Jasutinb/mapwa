
class State:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

class StateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[name]
        self.current_state.enter()

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)
