import sys
from pathlib import Path
import unittest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_icon_pr  # noqa: E402


def _make_icon(**overrides):
    """Return a valid devicon.json icon object with optional field overrides."""
    icon = {
        "name": "example",
        "altnames": [],
        "tags": ["tool"],
        "versions": {
            "svg": ["original", "plain"],
            "font": ["plain"],
        },
        "color": "#123456",
        "aliases": [],
    }
    icon.update(overrides)
    return icon


class CheckDeviconObjectAliasesTests(unittest.TestCase):
    """Regression tests for alias validation in check_icon_pr.check_devicon_object."""

    def test_valid_distinct_base_and_alias_passes(self):
        icon = _make_icon(aliases=[{"base": "original", "alias": "plain"}])
        self.assertEqual(check_icon_pr.check_devicon_object(icon), "")

    def test_same_base_and_alias_fails(self):
        icon = _make_icon(aliases=[{"base": "plain", "alias": "plain"}])
        result = check_icon_pr.check_devicon_object(icon)
        self.assertIn(
            '"base" and "alias" in "aliases" must have different values, got "plain" for both.',
            result,
        )

    def test_multiple_aliases_detects_matching_pair(self):
        icon = _make_icon(
            aliases=[
                {"base": "original", "alias": "plain"},
                {"base": "line-wordmark", "alias": "line-wordmark"},
            ]
        )
        result = check_icon_pr.check_devicon_object(icon)
        self.assertIn(
            '"base" and "alias" in "aliases" must have different values, got "line-wordmark" for both.',
            result,
        )

    def test_missing_alias_key_does_not_crash(self):
        icon = _make_icon(aliases=[{"base": "plain"}])
        result = check_icon_pr.check_devicon_object(icon)
        self.assertIn('missing key: "alias" in "aliases"', result)

    def test_missing_base_key_does_not_crash(self):
        icon = _make_icon(aliases=[{"alias": "plain"}])
        result = check_icon_pr.check_devicon_object(icon)
        self.assertIn('missing key: "base" in "aliases"', result)

    def test_empty_aliases_passes(self):
        icon = _make_icon(aliases=[])
        self.assertEqual(check_icon_pr.check_devicon_object(icon), "")


if __name__ == "__main__":
    unittest.main()
