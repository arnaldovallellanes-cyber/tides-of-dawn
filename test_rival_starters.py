from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]


class RivalStarterTests(unittest.TestCase):
    def test_all_seven_starter_variants_can_complete_baseline_rival_battles(self):
        for location in ("Route103", "Route110", "Route119", "LilycoveCity"):
            text = (ROOT / f"data/maps/{location}/scripts.inc").read_text()
            blocks = re.findall(r"switch VAR_STARTER_MON\n(.*?)\n\tend", text, re.S)
            self.assertEqual(len(blocks), 2, location)
            for block in blocks:
                choices = re.findall(r"case (\d+), (\w+)", block)
                self.assertEqual({int(choice) for choice, _ in choices}, set(range(7)), location)
                for _, label in choices:
                    self.assertRegex(text, rf"(?m)^{re.escape(label)}::?", location)


if __name__ == "__main__":
    unittest.main()
