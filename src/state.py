
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
        self.current_state_name = None

    def add_state(self, name, state):
        if name in self.states:
            raise ValueError(f"State already registered: {name}")
        self.states[name] = state

    def change_state(self, name):
        if name not in self.states:
            raise KeyError(f"Unknown state: {name}")
        if self.current_state_name == name:
            return False
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[name]
        self.current_state_name = name
        self.current_state.enter()
        return True

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)
