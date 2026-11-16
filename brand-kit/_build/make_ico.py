#!/usr/bin/env python3
"""Pack the size-tuned 16/32/48 renders into icons/favicon.ico (Pillow)."""
import os, sys
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
kit = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..")
frames = [Image.open(os.path.join(here, ".ico", f"ico-{s}.png")).convert("RGBA") for s in (16, 32, 48)]
frames[-1].save(os.path.join(kit, "icons", "favicon.ico"), format="ICO",
                sizes=[(16, 16), (32, 32), (48, 48)], append_images=frames[:-1])
print("favicon.ico", [im.size for im in frames])
