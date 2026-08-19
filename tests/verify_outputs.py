"""Host-side verification for final Blender deliverables."""

from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    ROOT / "rock_kingdom_fantasy_plaza.blend",
    ROOT / "renders" / "final_hero.png",
    ROOT / "renders" / "character_closeup.png",
    ROOT / "renders" / "plaza_wide.png",
]


def png_dimensions(path: Path):
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


failures = []
for path in EXPECTED:
    if not path.exists():
        failures.append(f"missing: {path}")
        continue
    if path.stat().st_size < 100_000:
        failures.append(f"file too small ({path.stat().st_size} bytes): {path}")
    if path.suffix.lower() == ".png":
        width, height = png_dimensions(path)
        if width < 960 or height < 600:
            failures.append(f"render too small ({width}x{height}): {path}")

if failures:
    raise SystemExit("OUTPUT_VERIFICATION_FAIL\n" + "\n".join(f" - {x}" for x in failures))

print("OUTPUT_VERIFICATION_PASS")
for path in EXPECTED:
    print(f" - {path.name}: {path.stat().st_size} bytes")
