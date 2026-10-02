import unittest
from scripts.validate_data import validate

class ValidationTests(unittest.TestCase):
    def data(self, problems):
        return {'competition': 'Example', 'years': [{'year': 2025, 'problems': problems}]}
    def test_valid_statement(self):
        self.assertEqual(validate(self.data([{'number': 1, 'problem': 'Prove $x=x$.'}]), 'Example.json'), [])
    def test_duplicate_identifier(self):
        p = {'number': 1, 'problem': 'Prove $x=x$.'}
        self.assertTrue(any('duplicate identifier' in e for e in validate(self.data([p, p]), 'Example.json')))
    def test_broken_formula(self):
        self.assertTrue(any('delimiter' in e for e in validate(self.data([{'number': 1, 'problem': 'Prove $x=x.'}]), 'Example.json')))
    def test_missing_figure(self):
        self.assertTrue(any('missing image' in e for e in validate(self.data([{'number': 1, 'problem': 'https://example.com/images/missing.png'}]), 'Example.json')))
    def test_gap_is_not_silently_renumbered(self):
        self.assertTrue(any('numbering' in e for e in validate(self.data([{'number': 2, 'problem': 'Find x.'}]), 'Example.json')))
    def test_control_character(self):
        self.assertTrue(any('control character' in e for e in validate(self.data([{'number': 1, 'problem': 'Find\x00 x.'}]), 'Example.json')))

if __name__ == '__main__':
    unittest.main()
