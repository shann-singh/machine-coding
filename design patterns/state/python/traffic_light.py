from abc import ABC, abstractmethod

# Abstract base class for Traffic Light States
class TrafficLightState(ABC):

    # Abstract method to define the transition to the next state
    @abstractmethod
    def next(self, context): pass

# Concrete state representing the Red Light
class RedLightState(TrafficLightState):

    def next(self, context):
        print("RED -> GREEN")  # Transition from Red to Green
        context.set_state(GreenLightState())

# Concrete state representing the Yellow Light
class YellowLightState(TrafficLightState):

    def next(self, context):
        print("YELLOW -> RED")  # Transition from Yellow to Red
        context.set_state(RedLightState())

# Concrete state representing the Green Light
class GreenLightState(TrafficLightState):

    def next(self, context):
        print("GREEN -> YELLOW")  # Transition from Green to Yellow
        context.set_state(YellowLightState())

# Context class to manage the current state of the Traffic Light
class TrafficLightContext:

    def __init__(self):
        self.state = RedLightState()  # Initial state is Red Light

    # Method to update the current state
    def set_state(self, state):
        self.state = state

    # Method to trigger the transition to the next state
    def next(self):
        self.state.next(self)

if __name__ == '__main__':
    # Create a Traffic Light Context
    traffic_light_context = TrafficLightContext()

    # Simulate state transitions
    traffic_light_context.next()  # Red -> Green
    traffic_light_context.next()  # Green -> Yellow
    traffic_light_context.next()  # Yellow -> Red
    traffic_light_context.next()  # Red -> Green
    traffic_light_context.next()  # Green -> Yellow