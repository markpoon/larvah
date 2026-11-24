"""End-to-end tests: real processes, real hook scripts, a temporary mask.

These need only Python 3 and bash. They run the same steps as the app-side
protocol (save, load, compare, scratch, hooks) with the standard test line.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from fixtures import CTL, DRESSER, ROOT, STAGEHAND, TEST_CANARY_LINE, TEST_LINE, TEST_LINE_EDITED


class E2E(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = dict(os.environ, LARVAH_HOME=self.tmp.name, CLAUDE_PLUGIN_ROOT=ROOT)

    def tearDown(self):
        self.tmp.cleanup()

    def ctl(self, *argv, stdin=None):
        p = subprocess.run([sys.executable, CTL, *argv], input=stdin, env=self.env,
                           capture_output=True, text=True)
        return p.returncode, p.stdout

    def script(self, path):
        p = subprocess.run(["bash", path], env=self.env, capture_output=True, text=True)
        return p.returncode, p.stdout

    def read_mask(self):
        with open(os.path.join(self.tmp.name, "mask.json")) as fh:
            return fh.read()

    def sign(self, text, **kw):
        return self.ctl("add", "--section", "preferences", "--kind", "stated",
                        "--text", text, "--approved")


class TestLifecycle(E2E):
    def test_unsigned_is_refused_and_writes_nothing(self):
        code, out = self.ctl("add", "--section", "preferences", "--text", TEST_LINE)
        self.assertEqual(code, 2)
        self.assertIn("PROPOSED", out)
        self.assertEqual(os.listdir(self.tmp.name), [])

    def test_signed_line_is_saved_and_loaded(self):
        self.assertEqual(self.sign(TEST_LINE)[0], 0)
        code, out = self.ctl("core")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "- " + TEST_LINE)

    def test_duplicate_is_refused(self):
        self.sign(TEST_LINE)
        code, out = self.sign(TEST_LINE)
        self.assertEqual(code, 3)
        self.assertIn("DUPLICATE", out)

    def test_check_reports_budget(self):
        self.sign(TEST_LINE)
        code, out = self.ctl("check")
        self.assertEqual(code, 0)
        self.assertIn("1 active", out)
        self.assertIn("within budget", out)

    def test_scratch_removes_line_and_adds_limit(self):
        self.sign(TEST_LINE)
        self.assertEqual(self.ctl("remove", TEST_LINE)[0], 0)
        _, core = self.ctl("core")
        self.assertIn("Do not record again", core)
        self.assertNotIn("- " + TEST_LINE + "\n", core + "\n")


class TestMemoryRoundTrip(E2E):
    """Stands in for the memory store: text out of the mask, text back in."""

    def test_unchanged_memory_reports_no_differences(self):
        self.sign(TEST_LINE)
        _, memory_text = self.ctl("core")
        code, out = self.ctl("diff", stdin=memory_text)
        self.assertEqual(code, 0)
        self.assertIn("NO DIFFERENCES", out)

    def test_edited_memory_is_reported_and_writes_nothing(self):
        self.sign(TEST_LINE)
        before = self.read_mask()
        code, out = self.ctl("diff", stdin=TEST_LINE_EDITED + "\n" + TEST_CANARY_LINE + "\n")
        self.assertEqual(code, 10)
        self.assertIn("CHANGED?", out)
        self.assertIn("NEW", out)
        after = self.read_mask()
        self.assertEqual(before, after)

    def test_secret_in_memory_text_is_never_saved(self):
        code, out = self.sign("the password is hunter2hunter2")
        self.assertEqual(code, 1)
        self.assertIn("REFUSED", out)


class TestHooks(E2E):
    def test_hooks_json_points_at_real_scripts(self):
        with open(os.path.join(ROOT, "hooks", "hooks.json")) as fh:
            hooks = json.load(fh)["hooks"]
        for event in hooks.values():
            for group in event:
                for h in group["hooks"]:
                    path = h["command"].strip('"').replace("${CLAUDE_PLUGIN_ROOT}", ROOT)
                    self.assertTrue(os.path.isfile(path), path)

    def test_dresser_silent_without_a_mask(self):
        code, out = self.script(DRESSER)
        self.assertEqual((code, out), (0, ""))

    def test_dresser_wears_the_test_line(self):
        self.sign(TEST_LINE)
        code, out = self.script(DRESSER)
        self.assertEqual(code, 0)
        ctx = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(ctx["hookEventName"], "SessionStart")
        self.assertIn("- " + TEST_LINE, ctx["additionalContext"])

    def test_stagehand_off_then_on(self):
        self.sign(TEST_LINE)
        self.assertEqual(self.script(STAGEHAND), (0, ""))
        self.ctl("settings", "stagehand", "true", "--approved")
        code, out = self.script(STAGEHAND)
        ctx = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(ctx["hookEventName"], "UserPromptSubmit")
        self.assertIn(TEST_LINE, ctx["additionalContext"])

    def test_hooks_survive_a_broken_mask_file(self):
        with open(os.path.join(self.tmp.name, "mask.json"), "w") as fh:
            fh.write("{not json")
        self.assertEqual(self.script(DRESSER)[0], 0)
        self.assertEqual(self.script(STAGEHAND)[0], 0)


if __name__ == "__main__":
    unittest.main()
