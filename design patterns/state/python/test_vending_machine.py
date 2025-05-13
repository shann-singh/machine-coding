import unittest
from vending_machine import VendingMachineContext, IdleState, HasMoneyState

class TestVendingMachine(unittest.TestCase):

    def setUp(self):
        self.vending_machine = VendingMachineContext()

    def test_initial_state(self):
        # Test that the initial state is IdleState
        self.assertIsInstance(self.vending_machine.state, IdleState)

    def test_insert_money(self):
        # Test inserting money transitions to HasMoneyState
        self.vending_machine.insert_money()
        self.assertIsInstance(self.vending_machine.state, HasMoneyState)

    def test_dispense_item_without_money(self):
        # Test dispensing item without inserting money
        with self.assertLogs() as log:
            self.vending_machine.dispense_item()
        self.assertIn("Insert money first.", log.output[0])
        self.assertIsInstance(self.vending_machine.state, IdleState)

    def test_dispense_item_with_money(self):
        # Test dispensing item after inserting money
        self.vending_machine.insert_money()
        with self.assertLogs() as log:
            self.vending_machine.dispense_item()
        self.assertIn("Item dispensed.", log.output[0])
        self.assertIsInstance(self.vending_machine.state, IdleState)

    def test_insert_money_twice(self):
        # Test inserting money twice
        self.vending_machine.insert_money()
        with self.assertLogs() as log:
            self.vending_machine.insert_money()
        self.assertIn("Already have money. Dispense item first.", log.output[0])
        self.assertIsInstance(self.vending_machine.state, HasMoneyState)

if __name__ == "__main__":
    unittest.main()
