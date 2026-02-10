import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from badusb.core import DuckyScript, PayloadGenerator

class TestDucky(unittest.TestCase):
    def test_parse(self):
        ds = DuckyScript()
        actions = ds.parse("STRING hello\nENTER\nDELAY 500")
        self.assertEqual(len(actions), 3)
        self.assertEqual(actions[0]["command"], "STRING")

class TestPayloadGen(unittest.TestCase):
    def test_templates(self):
        pg = PayloadGenerator()
        templates = pg.list_templates()
        self.assertIn("reverse_shell", templates)
        self.assertIn("recon", templates)

if __name__ == "__main__": unittest.main()
