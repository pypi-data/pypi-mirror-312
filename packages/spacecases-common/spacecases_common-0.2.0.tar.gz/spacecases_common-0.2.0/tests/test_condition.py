import unittest
from spacecases_common import Condition


class TestCondition(unittest.TestCase):
    def test_to_string(self):
        for input, expected in [
            (Condition.FACTORY_NEW, "Factory New"),
            (Condition.MINIMAL_WEAR, "Minimal Wear"),
            (Condition.FIELD_TESTED, "Field-Tested"),
            (Condition.WELL_WORN, "Well-Worn"),
            (Condition.BATTLE_SCARRED, "Battle-Scarred"),
        ]:
            self.assertEqual(str(input), expected)


if __name__ == "__main__":
    unittest.main()
