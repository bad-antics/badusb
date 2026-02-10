from badusb.core import DuckyScript, PayloadGenerator
pg = PayloadGenerator()
print("Templates:", pg.list_templates())
script = pg.generate("recon")
print("\nRecon payload:\n", script)
ds = DuckyScript()
actions = ds.parse(script)
print(f"\nParsed {len(actions)} actions")
