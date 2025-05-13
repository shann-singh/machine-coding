from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VendingMachineState(ABC):

    @abstractmethod
    def insert_money(self, context): pass

    @abstractmethod
    def dispense_item(self, context): pass

class IdleState(VendingMachineState):

    def insert_money(self, context):
        logger.info("Money inserted. Ready to Dispense.")
        context.set_state(HasMoneyState())
    
    def dispense_item(self, context):
        logger.info("Insert money first.")


class HasMoneyState(VendingMachineState):

    def insert_money(self, context):
        logger.info("Already have money. Dispense item first.")
    
    def dispense_item(self, context):
        logger.info("Item dispensed.")
        context.set_state(IdleState())

class VendingMachineContext:
    
    def __init__(self):
        self.state = IdleState()

    def set_state(self, state):
        self.state = state

    def insert_money(self):
        self.state.insert_money(self)

    def dispense_item(self):
        self.state.dispense_item(self)

if __name__ == '__main__':
    vending_machine = VendingMachineContext()
    vending_machine.dispense_item()
    vending_machine.insert_money()
    vending_machine.insert_money()
    vending_machine.dispense_item()
    vending_machine.insert_money()
    vending_machine.dispense_item()