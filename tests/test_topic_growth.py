"""New collections preserve audit snapshots without accepting stale reviews."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_topics import validate_topics


class TopicGrowthTests(unittest.TestCase):
    def test_import_preserves_historical_count_and_statement_binding(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'metadata').mkdir()
            (root / 'docs').mkdir()
            (root / 'index.html').write_text("key: 't', file: 'Example.json'\n")
            data = {'competition': 'Example', 'years': [{'year': 2025, 'problems': [
                {'number': 1, 'problem': 'Old statement.'},
                {'number': 2, 'problem': 'New collection statement.'}]}]}
            def write(name, value):
                (root / name).write_text(json.dumps(value))
            write('Example.json', data)
            sha = hashlib.sha256(b'Old statement.').hexdigest()
            write('metadata/topic-overrides.json', {'schema_version': 1, 'records': {
                't.2025.0.1': {'topics': ['Algebra'], 'reviewed_statement': 'Old statement.',
                    'statement_sha256': sha,
                    'review_method': 'AI-assisted full-statement thematic review'}}})
            audit = {'active_records': 1, 'reviewed_this_audit': 1,
                'not_reviewed_this_audit': 0, 'figures_inspected': [], 'reviews': {
                    't.2025.0.1': {'statement_sha256': sha,
                        'previous_topics': ['Algebra'], 'reviewed_topics': ['Algebra']}}}
            write('docs/topic-audit-example.json', audit)
            self.assertEqual(validate_topics(root), 1)
            data['years'][0]['problems'][0]['problem'] = 'Changed old statement.'
            write('Example.json', data)
            with self.assertRaisesRegex(AssertionError, 'stale thematic review'):
                validate_topics(root)
            data['years'][0]['problems'][0]['problem'] = 'Old statement.'
            write('Example.json', data)
            audit['active_records'] = 3
            write('docs/topic-audit-example.json', audit)
            with self.assertRaisesRegex(AssertionError, 'invalid historical bank count'):
                validate_topics(root)


if __name__ == '__main__':
    unittest.main()
