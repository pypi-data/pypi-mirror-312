import unittest
from spacecases_common import (
    Grade,
    CONSUMER_GRADE_COLOUR,
    INDUSTRIAL_GRADE_COLOUR,
    MIL_SPEC_COLOUR,
    RESTRICTED_COLOUR,
    CLASSIFIED_COLOUR,
    COVERT_COLOUR,
    CONTRABAND_COLOUR,
)


class TestGrade(unittest.TestCase):
    def test_to_string(self):
        for input, expected in [
            (Grade.CONSUMER_GRADE, "Consumer Grade"),
            (Grade.INDUSTRIAL_GRADE, "Industrial Grade"),
            (Grade.MIL_SPEC, "Mil-Spec"),
            (Grade.RESTRICTED, "Restricted"),
            (Grade.CLASSIFIED, "Classified"),
            (Grade.COVERT, "Covert"),
            (Grade.CONTRABAND, "Contraband"),
        ]:
            self.assertEqual(str(input), expected)

    def test_get_colour(self):
        for input, expected in [
            (Grade.CONSUMER_GRADE, CONSUMER_GRADE_COLOUR),
            (Grade.INDUSTRIAL_GRADE, INDUSTRIAL_GRADE_COLOUR),
            (Grade.MIL_SPEC, MIL_SPEC_COLOUR),
            (Grade.RESTRICTED, RESTRICTED_COLOUR),
            (Grade.CLASSIFIED, CLASSIFIED_COLOUR),
            (Grade.COVERT, COVERT_COLOUR),
            (Grade.CONTRABAND, CONTRABAND_COLOUR),
        ]:
            self.assertEqual(input.get_color(), expected)


if __name__ == "__main__":
    unittest.main()
