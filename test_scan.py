#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import unittest
import subprocess


class TestScanLogFiles(unittest.TestCase):
    def test_scan_has_tags(self):
        result = subprocess.run(
            ['python', 'scan_logfiles.py', 'scan', 'has_tags'],
            capture_output=True, text=True)
        self.assertIn('has_tags: True', result.stdout)

    def test_scan_tags_count(self):
        result = subprocess.run(
            ['python', 'scan_logfiles.py', 'scan', 'tags_count',
             '--count', '2'],
            capture_output=True, text=True)
        self.assertIn('tags_count: 2', result.stdout)

    def test_scan_has_volume(self):
        result = subprocess.run(
            ['python', 'scan_logfiles.py', 'scan', 'has_volume'],
            capture_output=True, text=True)
        self.assertIn('has_volume: True', result.stdout)

    def test_scan_has_note(self):
        result = subprocess.run(
            ['python', 'scan_logfiles.py', 'scan', 'has_note'],
            capture_output=True, text=True)
        # No records with note
        self.assertEqual('', result.stdout)


if __name__ == '__main__':
    unittest.main()
