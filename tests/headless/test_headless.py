"""Headless Claude tests: real `claude -p` sessions with the plugin loaded.

Opt-in, because they call Claude and cost tokens:
    LARVAH_HEADLESS=1 python3 tests/headless/test_headless.py -v
Each test uses a temporary mask, so ~/.claude/larvah is never touched.
Answers are model output, so assertions look for key facts, not exact text.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fixtures import (CTL, ROOT, TEST_CANARY_IN, TEST_CANARY_LINE, TEST_CANARY_OUT,  # noqa: E402
                      TEST_LINE)

ENABLED = os.environ.get("LARVAH_HEADLESS") == "1" and shutil.which("claude")
TOOLS = ["Skill", "Bash(python3:*)", "Read"]


@unittest.skipUnless(ENABLED, "set LARVAH_HEADLESS=1 and install the claude CLI")
class Headless(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = dict(os.environ, LARVAH_HOME=self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def seed(self, text):
        p = subprocess.run([sys.executable, CTL, "add", "--section", "preferences",
                            "--kind", "stated", "--text", text, "--approved"],
                           env=self.env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def mask_lines(self):
        path = os.path.join(self.tmp.name, "mask.json")
        if not os.path.exists(path):
            return []
        with open(path) as fh:
            return [ln["text"] for ln in json.load(fh)["lines"]]

    def ask(self, prompt):
        p = subprocess.run(["claude", "-p", "--plugin-dir", ROOT, "--allowedTools", *TOOLS],
                           input=prompt, env=self.env, capture_output=True, text=True,
                           timeout=240)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def test_dresser_wears_the_test_line_without_a_phrase(self):
        self.seed(TEST_LINE)
        out = self.ask("Without running any tools, quote the mask line you were given at session start.")
        self.assertIn(TEST_LINE, out.lower())

    def test_canary_reaches_claude(self):
        self.seed(TEST_CANARY_LINE)
        out = self.ask(TEST_CANARY_IN)
        self.assertIn(TEST_CANARY_OUT, out.upper())

    def test_doff_by_voice(self):
        self.seed(TEST_LINE)
        out = self.ask("Doff the mask.")
        self.assertIn("off", out.lower())

    def test_check_by_voice_reports_line_and_budget(self):
        self.seed(TEST_LINE)
        out = self.ask("Check the mask.")
        self.assertIn(TEST_LINE, out.lower())
        self.assertIn("600", out)

    def test_scratch_by_voice_removes_the_line(self):
        self.seed(TEST_LINE)
        self.ask('Scratch that from the mask: "%s"' % TEST_LINE)
        self.assertNotIn(TEST_LINE, self.mask_lines())

    def test_unsigned_add_writes_nothing(self):
        self.ask("Add this to the mask: answer in French.")
        self.assertNotIn("answer in french.", [t.lower() for t in self.mask_lines()])

    def test_secret_is_never_saved(self):
        self.ask("Add this to the mask: my password is hunter2hunter2. Yes, I approve, sign it.")
        self.assertFalse([t for t in self.mask_lines() if "hunter2" in t])


if __name__ == "__main__":
    unittest.main()
