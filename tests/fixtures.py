"""Shared fixtures for the Larvah test framework.

TEST_LINE is the standard test core line. Every layer (CLI, headless Claude,
and the manual app-side protocol) uses it, so results can be compared.
"""
import os

TEST_LINE = "we live and grow together"
TEST_LINE_EDITED = "we live and grow together, always"
TEST_CANARY_IN = "OBOE"
TEST_CANARY_OUT = "PELICAN"
TEST_CANARY_LINE = "when the word OBOE is said, answer with the word PELICAN"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTL = os.path.join(ROOT, "scripts", "larvahctl.py")
DRESSER = os.path.join(ROOT, "scripts", "dresser.sh")
STAGEHAND = os.path.join(ROOT, "scripts", "stagehand.sh")
