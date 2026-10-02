import unittest
from scripts.validate_data import validate, validate_statement_checks
import hashlib

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

class SourceCheckTests(unittest.TestCase):
    def test_stale_statement_check_is_rejected(self):
        text = 'Find $x$.'
        check = {'status':'statement_checked_against_source','reviewed_statement':text,
                 'statement_sha256':hashlib.sha256(text.encode()).hexdigest(),
                 'source_url':'https://example.com/exam.pdf','source_document_sha256':'a'*64,
                 'source_page':1,'source_problem_number':1,'checked_at':'2026-10-02',
                 'review_method':'AI-assisted visual and textual comparison','scope':'Statement fidelity only'}
        entry = {'statement_checks':{'test.2025.0.1':check}}
        data = {'years':[{'year':2025,'problems':[{'number':1,'problem':text}]}]}
        self.assertEqual(validate_statement_checks(entry,data,'test'), [])
        data['years'][0]['problems'][0]['problem']='Find $y$.'
        self.assertTrue(validate_statement_checks(entry,data,'test'))
    def test_reviewed_figure_change_is_rejected(self):
        from unittest.mock import patch
        from tempfile import TemporaryDirectory
        from pathlib import Path
        text = 'Figure: https://example.com/images/diagram.png'
        check = {'reviewed_statement': text, 'statement_sha256': hashlib.sha256(text.encode()).hexdigest(),
                 'figure_checks': [{'path':'images/diagram.png','sha256':hashlib.sha256(b'original').hexdigest()}]}
        entry = {'statement_checks': {'test.2025.0.1': check}}
        data = {'years':[{'year':2025,'problems':[{'number':1,'problem':text}]}]}
        with TemporaryDirectory() as folder, patch('scripts.validate_data.ROOT', Path(folder)):
            image = Path(folder) / 'images/diagram.png'
            image.parent.mkdir(); image.write_bytes(b'original')
            self.assertFalse(any('figure' in e for e in validate_statement_checks(entry,data,'test')))
            image.write_bytes(b'changed')
            self.assertTrue(any('figure changed' in e for e in validate_statement_checks(entry,data,'test')))
            check['figure_checks'] = []
            self.assertTrue(any('reviewed figure' in e for e in validate_statement_checks(entry,data,'test')))

    def test_wrong_checksum_is_rejected(self):
        entry = {'statement_checks':{'test.2025.0.1':{'reviewed_statement':'Find x.','statement_sha256':'bad'}}}
        data = {'years':[{'year':2025,'problems':[{'number':1,'problem':'Find x.'}]}]}
        self.assertTrue(any('checksum' in error for error in validate_statement_checks(entry,data,'test')))

if __name__ == '__main__':
    unittest.main()
